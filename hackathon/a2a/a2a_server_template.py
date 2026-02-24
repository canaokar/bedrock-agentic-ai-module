"""
Hackathon A2A Server Template
Wraps any Bedrock agent as an A2A-compatible service.
Adapt the SYSTEM_PROMPT and tools to match your agent's purpose.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import json
import uuid
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from bedrock_client import get_bedrock_client, CLAUDE_SONNET, converse_with_tools, extract_text

app = FastAPI()
client = get_bedrock_client()
tasks = {}

# --- Customize these for your agent ---
AGENT_CARD_PATH = os.path.join(os.path.dirname(__file__), "sample_agent_card.json")
SYSTEM_PROMPT = "You are a helpful research assistant. Provide detailed, accurate answers."
TOOLS = []  # Add your tool schemas here
TOOL_DISPATCH = {}  # Add your tool dispatch map here


class TaskRequest(BaseModel):
    message: str


class TaskResponse(BaseModel):
    id: str
    status: str
    result: str = None


@app.get("/.well-known/agent.json")
def get_agent_card():
    with open(AGENT_CARD_PATH) as f:
        return json.load(f)


@app.post("/tasks")
def create_task(request: TaskRequest):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "working", "result": None}

    try:
        if TOOLS:
            result, _ = converse_with_tools(
                client, CLAUDE_SONNET, SYSTEM_PROMPT, TOOLS, TOOL_DISPATCH, request.message
            )
        else:
            response = client.converse(
                modelId=CLAUDE_SONNET,
                system=[{"text": SYSTEM_PROMPT}],
                messages=[{"role": "user", "content": [{"text": request.message}]}],
            )
            result = extract_text(response["output"]["message"])

        tasks[task_id] = {"status": "completed", "result": result}
    except Exception as e:
        tasks[task_id] = {"status": "failed", "result": str(e)}

    return TaskResponse(id=task_id, **tasks[task_id])


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    if task_id not in tasks:
        return {"error": "Task not found"}
    return TaskResponse(id=task_id, **tasks[task_id])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
