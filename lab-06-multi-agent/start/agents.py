"""
Lab 06: Agent class for multi-agent orchestration.
Each agent wraps a Bedrock Converse call with its own system prompt and tools.
"""

import boto3
import os
from pathlib import Path

import json
import time

# Load .env file if it exists (so you don't have to export every time)
for _candidate in [
    Path(".env"),
    Path(__file__).resolve().parent / ".env",
    Path(__file__).resolve().parent.parent / ".env",
    Path(__file__).resolve().parent.parent.parent / "shared" / ".env",
]:
    if _candidate.exists():
        with open(_candidate) as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _key, _val = _line.split("=", 1)
                    os.environ.setdefault(_key.strip(), _val.strip())
        break

CLAUDE_SONNET = "global.anthropic.claude-sonnet-4-6"
CLAUDE_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
REGION = "ap-south-1"


def extract_text(message):
    for block in message.get("content", []):
        if "text" in block:
            return block["text"]
    return ""


class Agent:
    """A simple agent that wraps a Bedrock Converse call.

    Attributes:
        name: Human-readable agent name for logging.
        model_id: Bedrock model ID to use.
        system_prompt: Instructions for this agent.
        tools: List of tool schemas (optional).
        tool_dispatch: Dict mapping tool name to callable (optional).
    """

    def __init__(self, name, model_id, system_prompt, tools=None, tool_dispatch=None):
        """Initialize the agent.

        Args:
            name: Agent name for logging.
            model_id: Bedrock model ID.
            system_prompt: System instructions.
            tools: Optional list of Bedrock tool schemas.
            tool_dispatch: Optional dict mapping tool name to function.
        """
        # TODO: Store all attributes and create the bedrock client
        # Hint:
        #   self.name = name
        #   self.model_id = model_id
        #   self.system_prompt = system_prompt
        #   self.tools = tools or []
        #   self.tool_dispatch = tool_dispatch or {}
        #   self.client = boto3.client("bedrock-runtime", region_name=REGION)
        ...

    def run(self, prompt):
        """Run the agent with a user prompt, executing the full agent loop.

        Args:
            prompt: The task/question for this agent.

        Returns:
            The agent's final text response.
        """
        # TODO: Implement the agent loop (same pattern as Lab 02)
        # 1. Create messages list with user prompt
        # 2. Build converse kwargs (include toolConfig only if self.tools is non-empty)
        # 3. Loop: call converse, check stopReason
        #    - "end_turn": return extract_text(assistant_message)
        #    - "tool_use": dispatch tools, append results, continue
        # 4. Print timing: f"  [{self.name}] Done ({elapsed:.1f}s)"
        # Hint: start = time.time() at the beginning
        ...
