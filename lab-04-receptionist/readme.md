# Lab 04: Build a Receptionist

Build an intent-classifying receptionist that routes to specialist agents — the pattern behind real-world chatbot systems like ORCA/Cora.

## Objectives

- Define intent categories for a banking chatbot
- Build an intent classifier using Claude Haiku (fast, cheap SLM)
- Implement specialist handlers with their own tools and prompts
- Route classified messages to the correct specialist
- Add fallback logic for low-confidence classifications

---

## Prerequisites

- Labs 01-03 complete
- Understand the agent loop and tool dispatch

---

## Step 1: Define Intent Categories

Implement TODO 1 in `start/main.py`.

### What you are building

A dictionary of intent categories (faq, account_query, payment_help, tech_support, general) with descriptions that the classifier will use.

---

## Step 2: Build the Intent Classifier

Implement TODOs 2-3 in `start/main.py`.

### What you are building

A classifier that uses **Claude Haiku** (fast, cheap) to analyze user messages and return structured JSON with the intent, confidence score, and extracted entities.

### Key concepts

- **SLM for classification**: Haiku is ideal — classification is a simple task that doesn't need the power of Sonnet
- **Structured JSON output**: instruct the model to return only JSON for reliable parsing
- **Confidence scores**: let the model express uncertainty so we can handle edge cases

### Checkpoint

Test with "What are your hours?" — should classify as `faq` with high confidence.

---

## Step 3: Implement Specialist Handlers

Open `start/specialists.py` and implement the remaining specialists.

### What you are building

Specialist agents, each with its own system prompt and tools:
- **FAQ**: search_faq tool (provided complete as reference)
- **Account**: check_balance, get_transactions tools
- **Payment**: check_payment_status, initiate_transfer tools
- **General**: simple conversation, no tools

### Key concepts

- Each specialist is a mini-agent with focused expertise
- **Sonnet for generation**: specialists use the more capable model for quality responses
- Tools are domain-specific to each specialist

### Checkpoint

Test `handle_faq("What are your hours?")` directly — should return a response about branch hours.

---

## Step 4: Build the Router

Implement TODOs 4-5 in `start/main.py`.

### What you are building

A routing function that maps the classified intent to the correct specialist handler.

### Checkpoint

The full flow works: user message → classify → route → specialist response.

---

## Step 5: Add Fallback Logic

Implement TODO 6 in `start/main.py`.

### What you are building

When the classifier has low confidence (< 0.7), ask the user to clarify instead of routing to a potentially wrong specialist.

### Key concepts

- **Confidence threshold**: don't route uncertain messages
- **Graceful degradation**: ask for clarification rather than giving a wrong answer

### Checkpoint

"Tell me a joke" should trigger low confidence and a clarification request.

---

## Step 6: Multi-Turn Context

Implement TODO 7 in `start/main.py`.

### What you are building

A chat loop that maintains separate conversation histories per specialist.

---

## Step 7 (Stretch): Transfer Mechanism

Implement TODO 8 — allow a specialist to say "I can't handle this" and route back to the receptionist.

---

## Recap

| Step | What you built | Key takeaway |
|------|---------------|--------------|
| 1 | Intent categories | Define the routing targets |
| 2-3 | Intent classifier | Haiku (SLM) for fast, cheap classification |
| 3 | Specialist handlers | Sonnet (LLM) with domain-specific tools |
| 4-5 | Router | Maps intent → handler function |
| 6 | Fallback | Handle uncertainty gracefully |
| 7 | Multi-turn | Per-specialist conversation memory |
