"""
Lab 08 - A2A Client (Solution)
================================
Complete A2A client with agent discovery, task delegation, and polling.
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
async def fetch_agent_card(base_url: str) -> dict:
    """Fetch the agent card from the well-known endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/.well-known/agent.json")
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------------------------
# TODO 2 - Parse capabilities
# ---------------------------------------------------------------------------
def show_capabilities(card: dict):
    """Display the agent's capabilities and skills."""
    print(f"Agent: {card['name']}")
    print(f"Description: {card['description']}")
    print(f"Version: {card.get('version', 'N/A')}")

    caps = card.get("capabilities", {})
    print(f"Streaming: {caps.get('streaming', False)}")
    print(f"Push Notifications: {caps.get('pushNotifications', False)}")

    skills = card.get("skills", [])
    print(f"\nSkills ({len(skills)}):")
    for skill in skills:
        print(f"  - {skill['name']}: {skill['description']}")


# ---------------------------------------------------------------------------
# TODO 3 - Send a task
# ---------------------------------------------------------------------------
async def send_task(base_url: str, message: str, sender: str = "a2a-client") -> dict:
    """Send a task to the agent and return the response."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{base_url}/tasks",
            json={"message": message, "sender": sender},
        )
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------------------------
# TODO 4 - Poll for task completion
# ---------------------------------------------------------------------------
async def poll_task(base_url: str, task_id: str, interval: float = 1.0, max_attempts: int = 30) -> dict:
    """Poll for task completion with a timeout."""
    async with httpx.AsyncClient() as client:
        for _ in range(max_attempts):
            response = await client.get(f"{base_url}/tasks/{task_id}")
            data = response.json()
            if data["status"] in ("completed", "failed"):
                return data
            print(f"  Status: {data['status']}... waiting")
            await asyncio.sleep(interval)
    raise TimeoutError(f"Task {task_id} did not complete within {max_attempts * interval}s")


# ---------------------------------------------------------------------------
# TODO 5 - (BONUS) Multi-agent directory
# ---------------------------------------------------------------------------
class AgentDirectory:
    """A directory of A2A agents for multi-agent routing."""

    def __init__(self):
        self.agents: dict[str, dict] = {}  # name -> {"url": ..., "card": ...}

    async def register(self, url: str):
        """Discover and register an agent by URL."""
        card = await fetch_agent_card(url)
        name = card["name"]
        self.agents[name] = {"url": url, "card": card}
        print(f"Registered agent: {name} at {url}")

    def list_agents(self):
        """List all registered agents."""
        for name, info in self.agents.items():
            print(f"  {name}: {info['card']['description']}")

    def find_agent_for_skill(self, skill_keyword: str) -> str | None:
        """Find an agent URL that matches a skill keyword."""
        for name, info in self.agents.items():
            for skill in info["card"].get("skills", []):
                if skill_keyword.lower() in skill.get("description", "").lower():
                    return info["url"]
        return None

    async def delegate(self, skill_keyword: str, message: str) -> dict:
        """Route a task to the agent with a matching skill."""
        url = self.find_agent_for_skill(skill_keyword)
        if not url:
            raise ValueError(f"No agent found with skill matching: {skill_keyword}")
        print(f"Delegating to agent at {url}")
        return await send_task(url, message)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main():
    print("A2A Client - Lab 08 (Solution)")
    print("=" * 50)

    base_url = DEFAULT_AGENT_URL

    # Step 1: Discover the agent
    print("\n[1] Fetching agent card...")
    card = await fetch_agent_card(base_url)

    # Step 2: Show capabilities
    print("\n[2] Agent Capabilities:")
    show_capabilities(card)

    # Step 3: Send a task
    print("\n[3] Sending task...")
    task = await send_task(
        base_url,
        "What are three key factors to consider when evaluating a bank stock?",
    )
    print(f"Task ID: {task['task_id']}")
    print(f"Status: {task['status']}")

    # Step 4: If not already completed, poll for it
    if task["status"] not in ("completed", "failed"):
        print("\n[4] Polling for completion...")
        task = await poll_task(base_url, task["task_id"])

    # Print the result
    print(f"\n[Result] Status: {task['status']}")
    if task.get("result"):
        print(f"Response:\n{task['result']}")

    # Bonus: demonstrate the directory (uncomment if running multiple agents)
    # print("\n[5] Multi-agent directory demo:")
    # directory = AgentDirectory()
    # await directory.register("http://localhost:8000")
    # directory.list_agents()
    # result = await directory.delegate("finance", "Explain P/E ratio")
    # print(f"Delegated result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
