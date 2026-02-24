"""
Hackathon Tool: Translator
Uses Bedrock to translate text between languages.
"""

import json
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from bedrock_client import get_bedrock_client, CLAUDE_HAIKU, extract_text

TOOL_SCHEMA = {
    "toolSpec": {
        "name": "translate_text",
        "description": "Translate text from one language to another.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to translate"},
                    "target_language": {"type": "string", "description": "Target language (e.g., 'Spanish', 'French')"},
                    "source_language": {"type": "string", "description": "Source language (default: auto-detect)"}
                },
                "required": ["text", "target_language"]
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


def translate_text(text, target_language, source_language="auto-detect"):
    """Translate text using Bedrock Haiku."""
    client = _get_client()
    source_note = f" from {source_language}" if source_language != "auto-detect" else ""
    response = client.converse(
        modelId=CLAUDE_HAIKU,
        system=[{"text": f"Translate the following text{source_note} to {target_language}. "
                         f"Return only the translated text, nothing else."}],
        messages=[{"role": "user", "content": [{"text": text}]}],
    )
    translation = extract_text(response["output"]["message"])
    return json.dumps({"original": text, "translated": translation, "target_language": target_language})
