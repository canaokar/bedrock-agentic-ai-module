"""
Lab 05c: Strands Agent
Rebuild the agent using AWS Strands Agents SDK — minimal code with @tool decorators.
"""

# TODO 1: Import Strands Agent and tool decorator
# Hint:
#   from strands import Agent
#   from strands.tools import tool
import json

CLAUDE_SONNET = "us.anthropic.claude-sonnet-4-20250514"


# --- Tool: get_weather (PROVIDED COMPLETE as reference) ---
# @tool
# def get_weather(city: str) -> str:
#     """Get the current weather for a city.
#
#     Args:
#         city: The city name, e.g. 'London'
#     """
#     weather_data = {
#         "London": {"temp_c": 12, "condition": "Cloudy"},
#         "New York": {"temp_c": 22, "condition": "Sunny"},
#         "Mumbai": {"temp_c": 33, "condition": "Humid"},
#     }
#     data = weather_data.get(city, {"temp_c": 20, "condition": "Unknown"})
#     return json.dumps({"city": city, **data})


# TODO 2: Define search_news and get_time tools using @tool decorator
# Follow the get_weather pattern above.
# - search_news(query: str) -> str: returns JSON with fake news headlines
# - get_time(timezone: str) -> str: returns JSON with current time
# Remember: Strands uses the function docstring as the tool description.
...


# TODO 3: Create the Strands Agent
# Hint:
#   agent = Agent(
#       model=CLAUDE_SONNET,
#       tools=[get_weather, search_news, get_time],
#       system_prompt="You are a helpful assistant with access to tools."
#   )
...


# TODO 4: Run the agent with a user message
# Hint:
#   response = agent("What's the weather in London?")
#   print(response)
...


# TODO 5: Compare lines of code with Lab 02
# Count the lines in this file vs lab-02-first-agent/solution/main.py + tools.py
# Add a comment noting the difference.
...


# TODO 6 (BONUS): Try Strands built-in tools
# Import and use tools from strands_agents_tools if available.
# Example: from strands_agents_tools import file_read
...


if __name__ == "__main__":
    # Uncomment after implementing TODOs 1-4:
    # print("=== Single Query ===")
    # response = agent("What's the weather in London and any recent news about banking?")
    # print(f"Agent: {response}")
    #
    # print("\n=== Code Comparison ===")
    # print("Lab 02 (raw Bedrock): ~80 lines for agent loop + tools")
    # print("Lab 05c (Strands):    ~40 lines for the same functionality")
    pass
