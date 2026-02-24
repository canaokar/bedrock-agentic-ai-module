"""
Lab 08 - A2A Server (Start)
=============================
Build an A2A (Agent-to-Agent) server using FastAPI that follows the
A2A protocol: agent card discovery, task creation, and task retrieval.

Your tasks:
  TODO 1 - Serve the agent card at GET /.well-known/agent.json
  TODO 2 - Accept tasks at POST /tasks
  TODO 3 - Return task status at GET /tasks/{task_id}
  TODO 4 - Wire in a Bedrock agent to process the task
"""

import json
import uuid
from datetime import datetime
from typing import Optional

import boto3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CLAUDE_SONNET = "us.anthropic.claude-sonnet-4-20250514"
CLAUDE_HAIKU = "us.anthropic.claude-haiku-4-20250514"
REGION = "ap-south-1"
MODEL_ID = CLAUDE_HAIKU

bedrock = boto3.client("bedrock-runtime", region_name=REGION)

app = FastAPI(title="A2A Agent Server")

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------
class TaskRequest(BaseModel):
    """Incoming task request from another agent."""
    message: str
    sender: Optional[str] = None
    metadata: Optional[dict] = None


class TaskResponse(BaseModel):
    """Response returned for a task."""
    task_id: str
    status: str  # "pending", "completed", "failed"
    result: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None


# In-memory task store
tasks: dict[str, TaskResponse] = {}


# ---------------------------------------------------------------------------
# TODO 1 - Serve the agent card
# ---------------------------------------------------------------------------
# Create a GET endpoint at /.well-known/agent.json that reads and returns
# the agent_card.json file.
#
# Hint:
#   @app.get("/.well-known/agent.json")
#   async def get_agent_card():
#       with open("agent_card.json") as f:
#           return json.load(f)


# ---------------------------------------------------------------------------
# TODO 2 - Accept tasks
# ---------------------------------------------------------------------------
# Create a POST endpoint at /tasks that:
#   - Accepts a TaskRequest body
#   - Creates a TaskResponse with a unique ID and status="pending"
#   - Stores it in the tasks dict
#   - Calls process_task() to get the result (TODO 4)
#   - Updates the task with the result and status="completed"
#   - Returns the TaskResponse
#
# Hint:
#   @app.post("/tasks", response_model=TaskResponse)
#   async def create_task(request: TaskRequest):
#       task_id = str(uuid.uuid4())
#       ...


# ---------------------------------------------------------------------------
# TODO 3 - Return task status
# ---------------------------------------------------------------------------
# Create a GET endpoint at /tasks/{task_id} that:
#   - Looks up the task in the tasks dict
#   - Returns 404 if not found
#   - Returns the TaskResponse if found
#
# Hint:
#   @app.get("/tasks/{task_id}", response_model=TaskResponse)
#   async def get_task(task_id: str):
#       ...


# ---------------------------------------------------------------------------
# TODO 4 - Wire in Bedrock agent
# ---------------------------------------------------------------------------
# Write a function that takes a message string and returns a response
# from Bedrock. This is the "brain" behind your A2A agent.
#
# def process_task(message: str) -> str:
#     response = bedrock.converse(
#         modelId=MODEL_ID,
#         messages=[{"role": "user", "content": [{"text": message}]}],
#     )
#     return response["output"]["message"]["content"][0]["text"]


# ---------------------------------------------------------------------------
# Run the server
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
