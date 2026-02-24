"""
Lab 05c: Strands Agent (Solution)
# Lab 02 (raw Bedrock): ~80 lines for agent loop + tools
# Lab 05c (Strands):    ~40 lines for the same functionality
"""

from strands import Agent
from strands.tools import tool
import json
from datetime import datetime

CLAUDE_SONNET = "us.anthropic.claude-sonnet-4-20250514"


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: The city name, e.g. 'London'
    """
    weather_data = {
        "London": {"temp_c": 12, "condition": "Cloudy"},
        "New York": {"temp_c": 22, "condition": "Sunny"},
        "Mumbai": {"temp_c": 33, "condition": "Humid"},
    }
    data = weather_data.get(city, {"temp_c": 20, "condition": "Unknown"})
    return json.dumps({"city": city, **data})


@tool
def search_news(query: str) -> str:
    """Search for recent news articles on a topic.

    Args:
        query: The search query for news
    """
    headlines = [
        f"New {query} regulations announced by FCA",
        f"Major banks update {query} policies ahead of 2025 deadline",
    ]
    return json.dumps({"query": query, "headlines": headlines})


@tool
def get_time(timezone: str) -> str:
    """Get the current time in a given timezone.

    Args:
        timezone: The timezone, e.g. 'UTC', 'EST', 'GMT'
    """
    return json.dumps({"timezone": timezone, "time": datetime.now().strftime("%H:%M:%S")})


agent = Agent(
    model=CLAUDE_SONNET,
    tools=[get_weather, search_news, get_time],
    system_prompt="You are a helpful assistant with access to tools. Use them to answer questions accurately.",
)

if __name__ == "__main__":
    print("=== Single Query ===")
    response = agent("What's the weather in London and any recent news about banking?")
    print(f"Agent: {response}")

    print("\n=== Code Comparison ===")
    print("Lab 02 (raw Bedrock): ~80 lines for agent loop + tools")
    print("Lab 05c (Strands):    ~40 lines for the same functionality")
    print("That's the power of a framework — less boilerplate, same capability.")
