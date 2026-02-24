# Lab 06: Multi-Agent System

Build a multi-agent system using the supervisor pattern — a supervisor delegates to research, writer, and reviewer agents.

## Objectives

- Build a reusable Agent class wrapping Bedrock Converse
- Define specialist agents with different models and roles
- Implement a supervisor orchestration pipeline
- Use mixed models: Haiku for speed, Sonnet for quality

---

## Prerequisites

- Labs 01-04 complete (understand agent loop and tool dispatch)

---

## Step 1: Build the Agent Class

Open `start/agents.py` and implement the TODOs.

### What you are building

A reusable `Agent` class with `__init__()` and `run(prompt)` methods. Each agent has its own name, model, system prompt, and optional tools.

### Key concepts

- **Encapsulation**: each agent is a self-contained unit
- **Agent loop**: same pattern as Lab 02, but wrapped in a class
- **Reusability**: create different agents by changing the constructor arguments

### Checkpoint

```python
from agents import Agent, CLAUDE_HAIKU
agent = Agent("test", CLAUDE_HAIKU, "You are helpful.")
print(agent.run("Say hello"))
```

---

## Step 2: Define the Supervisor

Implement TODO 1 in `start/main.py`.

### What you are building

A supervisor agent that coordinates the pipeline — it receives the user's task but doesn't do the work directly.

---

## Step 3: Define Specialist Agents

Implement TODOs 2-3 in `start/main.py`.

### Key concepts

- **Research agent**: uses Haiku (fast/cheap) with search tools
- **Writer agent**: uses Sonnet (quality) for content generation
- **Different models for different roles**: optimize cost and quality

---

## Step 4: Build the Orchestration

Implement TODO 4 in `start/main.py`.

### What you are building

A pipeline: research -> write -> (review). Each agent's output feeds into the next.

### Checkpoint

Run the pipeline — you should see each agent running in sequence with timing.

---

## Step 5: Add the Reviewer

Implement TODO 5 — add a reviewer agent that critiques the draft.

---

## Step 6: Mixed Models

Implement TODO 6 — print a summary showing which model each agent used and the cost implications.

---

## Step 7 (Stretch): Parallel Execution

Implement TODO 7 — use `concurrent.futures` to run independent agents simultaneously.

---

## Recap

| Step | What you built | Key takeaway |
|------|---------------|--------------|
| 1 | Agent class | Reusable agent wrapper |
| 2-3 | Specialist agents | Different models for different roles |
| 4 | Orchestration | Pipeline: research -> write |
| 5 | Reviewer | Quality feedback loop |
| 6 | Mixed models | Haiku for speed, Sonnet for quality |
| 7* | Parallel execution | concurrent.futures for speedup |
