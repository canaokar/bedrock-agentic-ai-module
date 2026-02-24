# Lab 05c: Strands Agent

Rebuild the agent using AWS Strands Agents SDK — see how a framework reduces boilerplate with `@tool` decorators and an automatic agent loop.

## Objectives

- Define tools using the `@tool` decorator
- Create an Agent with a model and tools list
- Run the agent and observe the automatic agent loop
- Compare code volume with the raw Bedrock approach (Lab 02)

---

## Prerequisites

- Lab 02 complete (understand the raw agent loop)
- Install: `pip install -r start/requirements.txt`

---

## Step 1: Define Tools with Decorators

Implement TODOs 1-2 in `start/main.py`.

### What you are building

Tools using the Strands `@tool` decorator — Strands reads the function signature and docstring to generate the tool schema automatically.

### Key concepts

- **@tool decorator**: converts a Python function into a tool the agent can call
- **Docstrings matter**: Strands uses them as tool descriptions for the LLM
- **Type hints matter**: Strands uses them to generate the input schema

### Checkpoint

Your tools should be decorated functions with type hints and docstrings.

---

## Step 2: Create and Run the Agent

Implement TODOs 3-4 in `start/main.py`.

### Key concepts

- **Agent class**: wraps the Bedrock model, tools, and agent loop in one object
- **Automatic loop**: you don't write the while loop — Strands handles it
- **Same capability**: the agent can use tools, maintain context, and generate responses

### Checkpoint

The agent responds using tool results, just like Lab 02 — but with far less code.

---

## Step 3: Framework Comparison

Implement TODO 5.

### Key concepts

- Raw Bedrock (Lab 02): ~80 lines for agent loop + tools
- Strands (Lab 05c): ~40 lines for the same functionality
- Trade-off: less code but less control over the agent loop

---

## Step 4 (Stretch): Built-in Tools

Implement TODO 6 — explore tools from the `strands-agents-tools` package.

---

## Recap

| Step | What you built | Key takeaway |
|------|---------------|--------------|
| 1 | @tool functions | Decorators auto-generate tool schemas |
| 2 | Agent with tools | Automatic agent loop — no while loop needed |
| 3 | Comparison | ~50% less code with framework |
| 4* | Built-in tools | Strands provides common tools out of the box |
