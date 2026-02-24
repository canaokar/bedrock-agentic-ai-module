# Lab 02: Build Your First Agent

Build a tool-using agent from scratch using the Bedrock Converse API agent loop. This is the foundational pattern for everything that follows.

## Objectives

- Define tool schemas in the Bedrock Converse API format
- Implement mock tool functions
- Build the agent loop: LLM call -> tool dispatch -> result feedback -> repeat
- Understand stopReason, toolUse, and toolResult message structures
- Add interactive chat with conversation memory

---

## Prerequisites

- Lab 01 complete
- Comfortable with `client.converse()` calls

---

## Step 1: Define Tool Schemas

Open `start/tools.py` and implement TODOs 1-2.

### What you are building

JSON schemas that tell the LLM what tools are available and what parameters they accept. The `WEATHER_TOOL` is provided as a reference pattern.

### Key concepts

- **toolSpec**: each tool needs a `name`, `description`, and `inputSchema` (JSON Schema format)
- **inputSchema**: defines the parameters the tool accepts (type, description, required fields)
- **The LLM reads these schemas** to decide which tool to call and with what parameters

### Checkpoint

Your `NEWS_TOOL` and `TIME_TOOL` should follow the same structure as `WEATHER_TOOL`.

---

## Step 2: Implement Mock Tools

Implement TODOs 3-4 in `start/tools.py`.

### What you are building

Mock functions that return realistic fake data. In production, these would call real APIs.

### Key concepts

- Tools return **JSON strings** (the LLM parses the result)
- Mock data should be realistic enough for the LLM to formulate good responses
- Each function receives keyword arguments matching the tool schema

### Checkpoint

```python
from tools import search_news, get_time
print(search_news(query="banking"))  # Should print JSON with headlines
print(get_time(timezone="UTC"))       # Should print JSON with current time
```

---

## Step 3: Build the Agent Loop

Open `start/main.py` and implement TODOs 5-6.

### What you are building

The core agent loop — the most important pattern in this entire module:

```
User message → LLM (with tools) →
  if tool_use: execute tool → feed result back → LLM again →
  if end_turn: return final response
```

### Key concepts

- **toolConfig**: `{"tools": ALL_TOOLS}` tells Bedrock what tools are available
- **stopReason**: `"tool_use"` means the model wants to call a tool; `"end_turn"` means it's done
- **toolUse block**: contains `toolUseId`, `name`, and `input` for the tool call
- **toolResult**: you execute the tool locally and feed the result back as a user message
- **The loop**: keep calling `converse()` with updated messages until `stopReason == "end_turn"`

### Checkpoint

Run `python start/main.py` and verify:
- You see `[Tool Call]` logs showing the model calling weather and/or news tools
- The final response incorporates tool results (mentions weather data, news headlines)

---

## Step 4: Interactive Chat

Implement TODO 7 in `start/main.py`.

### What you are building

An interactive chat loop that shares conversation history across turns, so the agent remembers previous interactions.

### Key concepts

- Pass the same `messages` list to `run_agent()` on each turn
- The agent sees the full history (including tool calls) on every turn
- This is the foundation for stateful agents

### Checkpoint

Uncomment the chat section and test multi-turn:
- Ask "What's the weather in London?"
- Follow up with "How about New York?" — the agent should understand the context

---

## Recap

| Step | What you built | Key takeaway |
|------|---------------|--------------|
| 1 | Tool schemas | Tools are JSON Schema definitions the LLM reads |
| 2 | Mock tools | Tools return JSON strings; mock data enables testing |
| 3 | Agent loop | The while loop checking stopReason is THE core pattern |
| 4 | Chat with memory | Sharing message history creates stateful agents |
