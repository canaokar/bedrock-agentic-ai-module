"""
Lab 02: Tool definitions and mock implementations (Solution).
"""

import json
from datetime import datetime

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

NEWS_TOOL = {
    "toolSpec": {
        "name": "search_news",
        "description": "Search for recent news articles on a topic.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for news"
                    }
                },
                "required": ["query"]
            }
        }
    }
}

TIME_TOOL = {
    "toolSpec": {
        "name": "get_time",
        "description": "Get the current time in a given timezone.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "The timezone, e.g. 'UTC', 'EST', 'GMT'"
                    }
                },
                "required": ["timezone"]
            }
        }
    }
}


def get_weather(city):
    """Mock weather function."""
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
    """Mock news search function."""
    headlines = [
        f"New regulatory framework for {query} announced by FCA",
        f"Major banks update {query} policies ahead of 2025 deadline",
        f"Industry experts weigh in on {query} best practices",
    ]
    return json.dumps({"query": query, "headlines": headlines})


def get_time(timezone):
    """Mock timezone function."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps({"timezone": timezone, "current_time": now})


ALL_TOOLS = [WEATHER_TOOL, NEWS_TOOL, TIME_TOOL]

TOOL_DISPATCH = {
    "get_weather": get_weather,
    "search_news": search_news,
    "get_time": get_time,
}
