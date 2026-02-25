"""
Hackathon Building Block: Strands Agent Template
A minimal Strands SDK agent with Bedrock.
Customize the tools and system prompt for your use case.

Based on Lab 05c.
"""

from strands import Agent
from strands.tools import tool
import json


# --- Define your tools ---
@tool
def search_knowledge(query: str) -> str:
    """Search a knowledge base for information.

    Args:
        query: The search query.
    """
    # Replace with your actual search logic
    return json.dumps({
        "results": [
            {"title": f"Result about {query}", "content": f"Information related to {query}..."}
        ]
    })


@tool
def get_data(item_id: str) -> str:
    """Look up data by ID.

    Args:
        item_id: The ID of the item to look up.
    """
    # Replace with your actual data lookup
    return json.dumps({"id": item_id, "name": "Sample Item", "status": "active"})


# --- Create the agent ---
agent = Agent(
    model="global.anthropic.claude-sonnet-4-6",
    tools=[search_knowledge, get_data],
    system_prompt="You are a helpful assistant with access to a knowledge base and data lookup tools.",
)

if __name__ == "__main__":
    response = agent("What information do you have about AML compliance?")
    print(f"\nAgent: {response}")
