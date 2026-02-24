# Lab 03: Smart Agent

Enhance the basic agent with production-quality patterns: ReAct prompting, error handling, and conversation summarization.

## Objectives

- Write a ReAct system prompt that improves agent reasoning
- Add structured output with visible thought process
- Handle tool errors gracefully with LLM-based recovery
- Implement conversation summarization for long sessions

---

## Prerequisites

- Lab 02 complete (understand the agent loop)

---

## Step 1: ReAct Prompting

Implement TODO 1 in `start/main.py`.

### What you are building

A system prompt that instructs the model to think step-by-step before acting: THINK -> ACT -> OBSERVE -> RESPOND.

### Key concepts

- **ReAct** (Reasoning + Acting): the model explains its reasoning before each tool call
- Better prompts produce better tool selection and more accurate answers
- The model's reasoning becomes visible and debuggable

### Checkpoint

Run the agent — you should see the model's reasoning before each tool call in its response.

---

## Step 2: Structured Output

Implement TODO 2 in `start/main.py`.

### What you are building

Instruct the model to wrap reasoning in `<thought>` tags, making the thinking process explicit and parseable.

### Checkpoint

The model's response should contain `<thought>...</thought>` sections showing its reasoning.

---

## Step 3: Error Handling

Implement TODO 3 in `start/main.py`.

### What you are building

Wrap tool execution in try/except so that when a tool fails, the error is fed back to the LLM as a tool result. The LLM can then recover gracefully.

### Key concepts

- Tools can fail (network errors, invalid input, missing data)
- Feed the error back as a `toolResult` so the LLM knows what happened
- The LLM can retry with different parameters or answer without the tool

### Checkpoint

Ask about stock prices (the `get_stock_price` tool deliberately fails). The agent should handle the error and still provide a useful response.

---

## Step 4: Conversation Summarization

Implement TODO 4 in `start/main.py`.

### What you are building

A function that compresses long conversation histories by summarizing older messages, keeping recent ones intact. This prevents context window overflow.

### Key concepts

- Context windows have limits — long conversations eventually exceed them
- Summarize older messages with a cheap model (Haiku) to save tokens
- Keep recent messages verbatim for accuracy

### Checkpoint

The function should return a shorter message list when history exceeds 10 messages.

---

## Step 5 (Stretch): Reflection

Implement TODO 5 in `start/main.py`.

### What you are building

A reflection step where the agent critiques its own answer and optionally revises it.

### Checkpoint

The reflection should identify strengths and weaknesses in the agent's response.

---

## Recap

| Step | What you built | Key takeaway |
|------|---------------|--------------|
| 1 | ReAct prompt | Better reasoning = better tool use |
| 2 | Structured output | Visible thinking aids debugging |
| 3 | Error handling | Feed errors back to LLM for recovery |
| 4 | Summarization | Compress history to manage context window |
| 5* | Reflection | Self-critique improves answer quality |
