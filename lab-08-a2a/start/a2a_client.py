"""
Lab 08 - A2A Client (Start)
=============================
Build an A2A client that discovers agents, reads their capabilities,
and delegates tasks to them.

Your tasks:
  TODO 1 - Fetch the agent card from a server
  TODO 2 - Parse the agent's capabilities and skills
  TODO 3 - Send a task to the agent
  TODO 4 - Poll for task completion
  TODO 5 - (BONUS) Build a multi-agent directory
"""

import asyncio
import httpx
import json

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_AGENT_URL = "http://localhost:8000"


# ---------------------------------------------------------------------------
# TODO 1 - Fetch the agent card
# ---------------------------------------------------------------------------
# Write an async function that fetches GET {base_url}/.well-known/agent.json
# and returns the parsed JSON.
#
# async def fetch_agent_card(base_url: str) -> dict:
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f"{base_url}/.well-known/agent.json")
#         response.raise_for_status()
#         return response.json()


# ---------------------------------------------------------------------------
# TODO 2 - Parse capabilities
# ---------------------------------------------------------------------------
# Write a function that takes an agent card dict and prints:
#   - Agent name and description
#   - Whether it supports streaming
#   - Each skill's name and description
#
# def show_capabilities(card: dict):
#     print(f"Agent: {card['name']}")
#     print(f"Description: {card['description']}")
#     ...


# ---------------------------------------------------------------------------
# TODO 3 - Send a task
# ---------------------------------------------------------------------------
# Write an async function that sends a POST to {base_url}/tasks with a
# JSON body containing the message, and returns the response JSON.
#
# async def send_task(base_url: str, message: str) -> dict:
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             f"{base_url}/tasks",
#             json={"message": message},
#         )
#         response.raise_for_status()
#         return response.json()


# ---------------------------------------------------------------------------
# TODO 4 - Poll for task completion
# ---------------------------------------------------------------------------
# Write an async function that polls GET {base_url}/tasks/{task_id}
# until the status is "completed" or "failed".
#
# async def poll_task(base_url: str, task_id: str, interval: float = 1.0) -> dict:
#     async with httpx.AsyncClient() as client:
#         while True:
#             response = await client.get(f"{base_url}/tasks/{task_id}")
#             data = response.json()
#             if data["status"] in ("completed", "failed"):
#                 return data
#             await asyncio.sleep(interval)


# ---------------------------------------------------------------------------
# TODO 5 - (BONUS) Multi-agent directory
# ---------------------------------------------------------------------------
# Build a simple directory that can register multiple agent URLs,
# discover their capabilities, and route tasks to the right agent
# based on skill matching.
#
# class AgentDirectory:
#     def __init__(self):
#         self.agents = {}  # name -> {"url": ..., "card": ...}
#
#     async def register(self, url: str):
#         card = await fetch_agent_card(url)
#         self.agents[card["name"]] = {"url": url, "card": card}
#
#     def find_agent_for_skill(self, skill_keyword: str) -> str | None:
#         for name, info in self.agents.items():
#             for skill in info["card"].get("skills", []):
#                 if skill_keyword.lower() in skill["description"].lower():
#                     return info["url"]
#         return None
#
#     async def delegate(self, skill_keyword: str, message: str) -> dict:
#         url = self.find_agent_for_skill(skill_keyword)
#         if not url:
#             raise ValueError(f"No agent found for skill: {skill_keyword}")
#         return await send_task(url, message)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main():
    print("A2A Client - Lab 08")
    print("=" * 40)

    # Wire together TODOs 1-4 here:
    # 1. Fetch the agent card
    # 2. Show capabilities
    # 3. Send a task
    # 4. Poll for completion and print the result
    pass


if __name__ == "__main__":
    asyncio.run(main())
