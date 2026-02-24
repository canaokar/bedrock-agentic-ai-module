"""
Lab 02: Tool definitions and mock implementations.
Define tool schemas for the Bedrock Converse API and implement mock tool functions.
"""

import json
from datetime import datetime

# ---------------------------------------------------------------------------
# Tool schema for get_weather — PROVIDED COMPLETE as a reference pattern
# ---------------------------------------------------------------------------
WEATHER_TOOL = {
    "toolSpec": {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g. 'London'"
                    }
                },
                "required": ["city"]
            }
        }
    }
}

# TODO 1: Define NEWS_TOOL schema for search_news(query)
# Follow the same pattern as WEATHER_TOOL above.
# The tool should accept a "query" parameter (string).
NEWS_TOOL = ...

# TODO 2: Define TIME_TOOL schema for get_time(timezone)
# The tool should accept a "timezone" parameter (string).
TIME_TOOL = ...


# ---------------------------------------------------------------------------
# Mock tool implementations
# ---------------------------------------------------------------------------

def get_weather(city):
    """Mock weather function. Returns realistic fake weather data."""
    weather_data = {
        "London": {"temp_c": 12, "condition": "Cloudy", "humidity": 78},
        "New York": {"temp_c": 22, "condition": "Sunny", "humidity": 45},
        "Mumbai": {"temp_c": 33, "condition": "Humid", "humidity": 85},
        "Edinburgh": {"temp_c": 8, "condition": "Rainy", "humidity": 82},
        "Singapore": {"temp_c": 31, "condition": "Thunderstorms", "humidity": 90},
    }
    data = weather_data.get(city, {"temp_c": 20, "condition": "Unknown", "humidity": 50})
    return json.dumps({"city": city, **data})


def search_news(query):
    """Mock news search function.

    Args:
        query: The search query string.

    Returns:
        A JSON string with 2-3 fake news headlines related to the query.
    """
    # TODO 3: Return a JSON string with fake news headlines
    # Hint: return json.dumps({"query": query, "headlines": [...]})
    ...


def get_time(timezone):
    """Mock timezone function.

    Args:
        timezone: The timezone name (e.g., 'UTC', 'EST', 'GMT').

    Returns:
        A JSON string with the current time.
    """
    # TODO 4: Return the current time as a JSON string
    # Hint: Use datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ...


# ---------------------------------------------------------------------------
# Collect all tools for easy import
# ---------------------------------------------------------------------------
ALL_TOOLS = [WEATHER_TOOL, NEWS_TOOL, TIME_TOOL]

TOOL_DISPATCH = {
    "get_weather": get_weather,
    "search_news": search_news,
    "get_time": get_time,
}
