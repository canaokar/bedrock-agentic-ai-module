"""
Lab 06: Agent class (Solution).
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
LLAMA = "meta.llama3-8b-instruct-v1:0"
MISTRAL = "mistral.ministral-3-3b-instruct"
REGION = "ap-south-1"


def extract_text(message):
    for block in message.get("content", []):
        if "text" in block:
            return block["text"]
    return ""


class Agent:
    def __init__(self, name, model_id, system_prompt, tools=None, tool_dispatch=None):
        self.name = name
        self.model_id = model_id
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.tool_dispatch = tool_dispatch or {}
        self.client = boto3.client("bedrock-runtime", region_name=REGION)

    def run(self, prompt):
        start = time.time()
        print(f"  [{self.name}] Running with {self.model_id.split('.')[-1].split('-')[0]}...")

        messages = [{"role": "user", "content": [{"text": prompt}]}]

        while True:
            kwargs = {
                "modelId": self.model_id,
                "system": [{"text": self.system_prompt}],
                "messages": messages,
            }
            if self.tools:
                kwargs["toolConfig"] = {"tools": self.tools}

            response = self.client.converse(**kwargs)
            msg = response["output"]["message"]
            messages.append(msg)

            if response["stopReason"] == "end_turn":
                elapsed = time.time() - start
                print(f"  [{self.name}] Done ({elapsed:.1f}s)")
                return extract_text(msg)

            if response["stopReason"] == "tool_use":
                results = []
                for block in msg["content"]:
                    if "toolUse" in block:
                        name = block["toolUse"]["name"]
                        inp = block["toolUse"]["input"]
                        tid = block["toolUse"]["toolUseId"]
                        try:
                            out = self.tool_dispatch[name](**inp)
                        except Exception as e:
                            out = json.dumps({"error": str(e)})
                        results.append({"toolResult": {"toolUseId": tid, "content": [{"text": str(out)}]}})
                messages.append({"role": "user", "content": results})
