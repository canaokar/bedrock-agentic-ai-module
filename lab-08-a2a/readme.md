# Lab 08: A2A Agent Network (Stretch)

## Objective

Build an **A2A (Agent-to-Agent)** server and client that follow the A2A protocol: agent card discovery, task creation, and task retrieval. This lab introduces inter-agent communication patterns.

## What You Will Learn

- How to publish an **agent card** at `/.well-known/agent.json`
- How to build a FastAPI server that accepts and processes tasks
- How to write a client that discovers agents and delegates work
- How to poll for asynchronous task completion
- (Bonus) How to build a multi-agent directory for routing

## Prerequisites

- Python 3.11+
- AWS credentials configured for Bedrock access
- `pip install -r requirements.txt`

## Files

| File | Description |
|------|-------------|
| `agent_card.json` | Agent metadata for A2A discovery |
| `a2a_server.py` | FastAPI server implementing the A2A protocol |
| `a2a_client.py` | Client that discovers agents and sends tasks |
| `requirements.txt` | Python dependencies |

## Tasks

### agent_card.json

Fill in the TODO placeholders with a meaningful agent name, description, and skill definitions.

### a2a_server.py (4 TODOs)

1. **TODO 1** - Serve the agent card at `GET /.well-known/agent.json`
2. **TODO 2** - Accept tasks at `POST /tasks`
3. **TODO 3** - Return task status at `GET /tasks/{task_id}`
4. **TODO 4** - Wire in a Bedrock agent to process the task

### a2a_client.py (5 TODOs)

1. **TODO 1** - Fetch the agent card from a server
2. **TODO 2** - Parse and display the agent's capabilities
3. **TODO 3** - Send a task to the agent
4. **TODO 4** - Poll for task completion
5. **TODO 5** - (BONUS) Build a multi-agent directory

## Running

```bash
# Terminal 1: Start the server
python a2a_server.py

# Terminal 2: Run the client
python a2a_client.py
```

## Key Concepts

- **Agent Card** is a JSON document describing an agent's identity, capabilities, and skills
- **Well-Known URI** (`/.well-known/agent.json`) is the standard discovery endpoint
- **Tasks** are the unit of work in A2A -- a client sends a message, the server processes it
- **Polling** lets the client check task status asynchronously
- **Agent Directory** enables routing tasks to the right agent based on skill matching
