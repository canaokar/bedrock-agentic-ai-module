"""
Hackathon A2A Client
Discovers and communicates with A2A-compatible agents.
"""

import httpx
import time
import json


def discover_agent(base_url):
    """Fetch and display an agent's capabilities from its agent card."""
    response = httpx.get(f"{base_url}/.well-known/agent.json")
    response.raise_for_status()
    card = response.json()

    print(f"Agent: {card['name']}")
    print(f"Description: {card['description']}")
    print(f"Skills:")
    for skill in card.get("skills", []):
        print(f"  - {skill['name']}: {skill['description']}")

    return card


def send_task(base_url, message):
    """Send a task to an A2A agent and wait for completion."""
    print(f"\nSending task: {message[:80]}...")
    response = httpx.post(f"{base_url}/tasks", json={"message": message})
    response.raise_for_status()
    task = response.json()
    task_id = task["id"]

    # Poll for completion if status is "working"
    while task.get("status") == "working":
        time.sleep(1)
        poll = httpx.get(f"{base_url}/tasks/{task_id}")
        task = poll.json()
        print(f"  Status: {task['status']}")

    print(f"\nResult ({task['status']}):")
    print(task.get("result", "No result"))
    return task


if __name__ == "__main__":
    BASE_URL = "http://localhost:8000"

    print("=== Discovering Agent ===")
    card = discover_agent(BASE_URL)

    print("\n=== Sending Task ===")
    result = send_task(BASE_URL, "What are the key requirements for AML compliance?")
