"""
Lab 08 - A2A Server (Solution)
================================
Complete A2A server with agent card, task endpoints, and Bedrock integration.
"""

import os
from pathlib import Path
import json
import uuid
from datetime import datetime, timezone
from typing import Optional

import boto3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load .env file if it exists (so you don't have to export every time)
for _candidate in [
    Path(".env"),
    Path(__file__).resolve().parent / ".env",
    Path(__file__).resolve().parent.parent / ".env",
    Path(__file__).resolve().parent.parent.parent / "shared" / ".env",
]:
    if _candidate.exists():
        with open(_candidate) as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _key, _val = _line.split("=", 1)
                    os.environ.setdefault(_key.strip(), _val.strip())
        break

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CLAUDE_SONNET = "global.anthropic.claude-sonnet-4-6"
CLAUDE_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
LLAMA = "meta.llama3-8b-instruct-v1:0"
MISTRAL = "mistral.ministral-3-3b-instruct"
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
    status: str
    result: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None


# In-memory task store
tasks: dict[str, TaskResponse] = {}


# ---------------------------------------------------------------------------
# TODO 4 - Bedrock agent processing
# ---------------------------------------------------------------------------
def process_task(message: str) -> str:
    """Send a message to Bedrock and return the response text."""
    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": message}]}],
    )
    return response["output"]["message"]["content"][0]["text"]


# ---------------------------------------------------------------------------
# TODO 1 - Serve the agent card
# ---------------------------------------------------------------------------
@app.get("/.well-known/agent.json")
async def get_agent_card():
    """Return the agent card for A2A discovery."""
    with open("agent_card.json") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# TODO 2 - Accept tasks
# ---------------------------------------------------------------------------
@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    """Create and process a new task."""
    task_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    # Create task in pending state
    task = TaskResponse(
        task_id=task_id,
        status="pending",
        created_at=now,
    )
    tasks[task_id] = task

    # Process the task using Bedrock
    try:
        result = process_task(request.message)
        task.status = "completed"
        task.result = result
        task.completed_at = datetime.now(timezone.utc).isoformat()
    except Exception as e:
        task.status = "failed"
        task.result = f"Error: {str(e)}"
        task.completed_at = datetime.now(timezone.utc).isoformat()

    return task


# ---------------------------------------------------------------------------
# TODO 3 - Return task status
# ---------------------------------------------------------------------------
@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Retrieve a task by ID."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")
    return tasks[task_id]


# ---------------------------------------------------------------------------
# Run the server
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
