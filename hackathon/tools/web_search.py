"""
Hackathon Tool: Web Search (Mock)
Simulates web search results for agent use.
"""

import json

TOOL_SCHEMA = {
    "toolSpec": {
        "name": "web_search",
        "description": "Search the web for information on a topic. Returns a list of search results.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        }
    }
}


def web_search(query):
    """Return mock web search results relevant to the query."""
    results = [
        {
            "title": f"Understanding {query} - Overview",
            "url": f"https://example.com/{query.replace(' ', '-').lower()}",
            "snippet": f"A comprehensive overview of {query}. This resource covers key concepts, "
                       f"best practices, and recent developments in {query}."
        },
        {
            "title": f"{query}: Latest News and Updates",
            "url": f"https://news.example.com/{query.replace(' ', '-').lower()}",
            "snippet": f"Recent developments in {query}. Industry experts weigh in on "
                       f"the latest trends and what they mean for the future."
        },
        {
            "title": f"Best Practices for {query}",
            "url": f"https://guide.example.com/{query.replace(' ', '-').lower()}",
            "snippet": f"A practical guide to {query} with step-by-step instructions, "
                       f"examples, and common pitfalls to avoid."
        },
    ]
    return json.dumps({"query": query, "results": results})
