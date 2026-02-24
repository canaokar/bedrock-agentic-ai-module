"""
Hackathon Tool: Summarizer
Uses Bedrock to summarize text.
"""

import json
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from bedrock_client import get_bedrock_client, CLAUDE_HAIKU, extract_text

TOOL_SCHEMA = {
    "toolSpec": {
        "name": "summarize_text",
        "description": "Summarize a piece of text into a concise version.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to summarize"},
                    "max_sentences": {
                        "type": "integer",
                        "description": "Maximum sentences in the summary (default 3)"
                    }
                },
                "required": ["text"]
            }
        }
    }
}

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = get_bedrock_client()
    return _client


def summarize_text(text, max_sentences=3):
    """Summarize text using Bedrock Haiku (fast and cheap)."""
    client = _get_client()
    response = client.converse(
        modelId=CLAUDE_HAIKU,
        system=[{"text": f"Summarize the following text in at most {max_sentences} sentences. "
                         f"Be concise and preserve key information."}],
        messages=[{"role": "user", "content": [{"text": text}]}],
    )
    summary = extract_text(response["output"]["message"])
    return json.dumps({"summary": summary})
