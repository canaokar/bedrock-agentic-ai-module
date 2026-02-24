"""
Hackathon Tool: Sentiment Analysis
Uses Bedrock to analyze sentiment of text.
"""

import json
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from bedrock_client import get_bedrock_client, CLAUDE_HAIKU, extract_text

TOOL_SCHEMA = {
    "toolSpec": {
        "name": "analyze_sentiment",
        "description": "Analyze the sentiment of a piece of text.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to analyze"}
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


def analyze_sentiment(text):
    """Analyze sentiment using Bedrock Haiku."""
    client = _get_client()
    response = client.converse(
        modelId=CLAUDE_HAIKU,
        system=[{"text": 'Analyze the sentiment of the text. Return ONLY a JSON object with keys: '
                         '"sentiment" (one of: positive, negative, neutral, mixed), '
                         '"confidence" (0.0 to 1.0), '
                         '"explanation" (one sentence).'}],
        messages=[{"role": "user", "content": [{"text": text}]}],
    )
    result_text = extract_text(response["output"]["message"])
    try:
        result = json.loads(result_text)
    except json.JSONDecodeError:
        result = {"sentiment": "unknown", "confidence": 0.0, "explanation": result_text}
    return json.dumps(result)
