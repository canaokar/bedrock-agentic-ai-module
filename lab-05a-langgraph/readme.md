# Lab 05a: LangGraph Agent

## Objectives

By the end of this lab you will be able to:

1. Define a **typed agent state** using Python `TypedDict`.
2. Express an intent-classification-and-dispatch workflow as a **LangGraph `StateGraph`**.
3. Use **conditional edges** to route between specialist nodes.
4. Compile and invoke the graph end-to-end against Amazon Bedrock.
5. (Bonus) Add **human-in-the-loop** interrupts and a **feedback loop**.

---

## Prerequisites

| Requirement | Details |
|---|---|
| **Lab 04 completed** | You should be comfortable with the receptionist pattern (classifier + specialist prompts + Bedrock Converse API). |
| **Python 3.11+** | Required for `TypedDict` features used in this lab. |
| **AWS credentials** | Bedrock access in `ap-south-1` with Claude Sonnet and Claude Haiku enabled. |
| **Dependencies** | Install with `pip install -r requirements.txt` |

---

## Architecture Overview

```
              +------------+
  User ------>|  classify   |
              +-----+------+
                    |  conditional edge (route_by_intent)
          +---------+---------+---------+
          v         v         v         v
       +-----+  +-------+  +-------+  +-------+
       | faq |  |account|  |payment|  |general|
       +--+--+  +---+---+  +---+---+  +---+---+
          |          |          |          |
          +----------+----------+----------+
                          |
                         END
```

---

## Steps

### Step 0 -- Setup

```bash
cd start/
pip install -r requirements.txt
```

Open `main.py` and read through the existing code: constants, system prompts, and the `call_bedrock` helper are already provided.

---

### Step 1 -- Define `AgentState` (TODO 1)

Create a `TypedDict` called `AgentState` with four fields:

| Field | Type | Purpose |
|---|---|---|
| `messages` | `list` | Conversation history (list of dicts with `role` and `content`) |
| `current_intent` | `str` | The classified intent label |
| `confidence` | `float` | Classifier confidence score (0.0 - 1.0) |
| `response` | `str` | The final answer to return to the customer |

```python
class AgentState(TypedDict):
    messages: list
    current_intent: str
    confidence: float
    response: str
```

---

### Step 2 -- Classifier Node (TODO 2)

Implement `classifier_node(state)`:

1. Extract the latest user message from `state["messages"]`.
2. Call `call_bedrock` with `CLAUDE_HAIKU` and `CLASSIFIER_SYSTEM_PROMPT`.
3. Parse the JSON response to get `intent` and `confidence`.
4. Return `{"current_intent": intent, "confidence": confidence}`.

**Tip:** Wrap the JSON parsing in a try/except -- if parsing fails, default to `"general"` with confidence `0.0`.

---

### Step 3 -- Specialist Nodes (TODO 3)

Create four functions: `faq_node`, `account_node`, `payment_node`, `general_node`.

Each follows the same pattern:

1. Get the latest user message from `state["messages"]`.
2. Call `call_bedrock` with `CLAUDE_SONNET` and the corresponding system prompt.
3. Return `{"response": answer}`.

---

### Step 4 -- Routing Function (TODO 4)

Implement `route_by_intent(state)`:

- If `state["confidence"] < 0.6`, return `"general"` (low-confidence fallback).
- Otherwise return `state["current_intent"]` if it is one of `"faq"`, `"account"`, `"payment"`.
- Default to `"general"` for any unrecognised intent.

---

### Step 5 -- Build the StateGraph (TODO 5)

```python
graph = StateGraph(AgentState)

graph.add_node("classify", classifier_node)
graph.add_node("faq", faq_node)
graph.add_node("account", account_node)
graph.add_node("payment", payment_node)
graph.add_node("general", general_node)

graph.set_entry_point("classify")
```

---

### Step 6 -- Add Edges and Compile (TODO 6)

```python
graph.add_conditional_edges(
    "classify",
    route_by_intent,
    {"faq": "faq", "account": "account", "payment": "payment", "general": "general"},
)

graph.add_edge("faq", END)
graph.add_edge("account", END)
graph.add_edge("payment", END)
graph.add_edge("general", END)

app = graph.compile()
```

Run `python main.py` and verify the three test queries are classified and answered.

---

### Step 7 (BONUS) -- Human-in-the-Loop (TODO 7)

Re-compile the graph with `interrupt_before` to pause execution before sensitive specialist nodes:

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app_with_hitl = graph.compile(
    checkpointer=memory,
    interrupt_before=["account", "payment"],
)
```

When the graph hits an interrupted node it will stop and return the current state. You can inspect the intent, ask the user for confirmation, then resume execution.

---

### Step 8 (BONUS) -- Feedback Loop (TODO 8)

Design a `feedback` node that:

1. Presents the specialist's response to the user.
2. Asks whether the answer was helpful.
3. If **yes** -- route to `END`.
4. If **no** -- update `state["messages"]` with additional context and route back to `"classify"`.

This introduces a **cycle** in the graph, which LangGraph supports natively.

---

## Key Concepts

| Concept | What It Means |
|---|---|
| **StateGraph** | A directed graph whose nodes read and write to a shared typed state dict. |
| **TypedDict** | A Python type hint that gives each state field a name and type, enabling IDE support and validation. |
| **Conditional Edges** | Edges whose target is determined at runtime by a routing function that inspects the current state. |
| **Entry Point** | The first node executed when the graph is invoked. |
| **Compile** | Finalises the graph structure and returns a runnable application object. |
| **interrupt_before** | A compile-time option that pauses the graph before specified nodes, enabling human-in-the-loop patterns. |

---

## Checkpoints

Use the following checklist to verify your implementation:

- [ ] `AgentState` TypedDict is defined with all four fields.
- [ ] `classifier_node` returns `current_intent` and `confidence`.
- [ ] All four specialist nodes return a `response` string.
- [ ] `route_by_intent` falls back to `"general"` for low confidence.
- [ ] The graph has five nodes and the entry point is `"classify"`.
- [ ] Conditional edges route from `"classify"` to the correct specialist.
- [ ] Each specialist has an edge to `END`.
- [ ] `python main.py` runs end-to-end and prints intent + response for all three test queries.

---

## Recap

| Step | What You Did |
|---|---|
| 1 | Defined a typed state schema for the agent |
| 2 | Built a classifier node that calls Haiku and parses JSON |
| 3 | Created four specialist nodes that call Sonnet |
| 4 | Wrote a routing function with confidence-based fallback |
| 5 | Assembled the StateGraph and registered all nodes |
| 6 | Wired conditional and normal edges, compiled the graph |
| 7 | (Bonus) Added human-in-the-loop interrupts |
| 8 | (Bonus) Designed a feedback cycle |

---

## Next Steps

- **Lab 05b** -- Explore LangGraph's built-in streaming and token callbacks.
- **Hackathon** -- Apply these patterns to build a multi-specialist agent for a domain of your choice.
