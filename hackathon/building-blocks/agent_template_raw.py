"""
Hackathon Building Block: Raw Bedrock Agent Template
A minimal tool-using agent built with the raw Bedrock Converse API.
Copy this file and customize the SYSTEM_PROMPT, tools, and tool functions.

Based on Lab 02.
"""

import boto3

import json

CLAUDE_SONNET = "global.anthropic.claude-sonnet-4-6"
CLAUDE_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
REGION = "ap-south-1"

# --- Customize these ---
SYSTEM_PROMPT = "You are a helpful assistant with access to tools."
MODEL_ID = CLAUDE_SONNET

# --- Define your tools ---
EXAMPLE_TOOL = {
    "toolSpec": {
        "name": "example_tool",
        "description": "An example tool. Replace with your own.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Input query"}
                },
                "required": ["query"]
            }
        }
    }
}


def example_tool(query):
    """Replace with your tool implementation."""
    return json.dumps({"result": f"You searched for: {query}"})


# Tool configuration
TOOLS = [EXAMPLE_TOOL]
TOOL_DISPATCH = {"example_tool": example_tool}


def extract_text(message):
    for block in message.get("content", []):
        if "text" in block:
            return block["text"]
    return ""


def run_agent(user_message, messages=None):
    """Run the agent loop with a user message. Returns (response_text, messages)."""
    client = boto3.client("bedrock-runtime", region_name=REGION)

    if messages is None:
        messages = []
    messages.append({"role": "user", "content": [{"text": user_message}]})

    while True:
        response = client.converse(
            modelId=MODEL_ID,
            system=[{"text": SYSTEM_PROMPT}],
            messages=messages,
            toolConfig={"tools": TOOLS},
        )
        assistant_msg = response["output"]["message"]
        messages.append(assistant_msg)

        if response["stopReason"] == "end_turn":
            return extract_text(assistant_msg), messages

        if response["stopReason"] == "tool_use":
            tool_results = []
            for block in assistant_msg["content"]:
                if "toolUse" in block:
                    name = block["toolUse"]["name"]
                    inp = block["toolUse"]["input"]
                    tid = block["toolUse"]["toolUseId"]
                    print(f"  [Tool] {name}({json.dumps(inp)})")
                    try:
                        result = TOOL_DISPATCH[name](**inp)
                    except Exception as e:
                        result = json.dumps({"error": str(e)})
                    tool_results.append({
                        "toolResult": {"toolUseId": tid, "content": [{"text": str(result)}]}
                    })
            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    response, _ = run_agent("Hello! What can you do?")
    print(f"\nAgent: {response}")
