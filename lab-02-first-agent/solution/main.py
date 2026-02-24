"""
Lab 02: Build Your First Agent (Solution)
"""

import boto3

import json
from tools import ALL_TOOLS, TOOL_DISPATCH

CLAUDE_SONNET = "global.anthropic.claude-sonnet-4-6"
CLAUDE_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
REGION = "ap-south-1"

SYSTEM_PROMPT = """You are a helpful assistant with access to tools.
Use the available tools to answer user questions accurately.
Always use tools when they can provide useful information."""


def get_client():
    return boto3.client("bedrock-runtime", region_name=REGION)


def extract_text(message):
    """Extract text content from a Bedrock response message."""
    for block in message.get("content", []):
        if "text" in block:
            return block["text"]
    return ""


def run_agent(client, user_message, messages=None):
    """Run the agent loop: call LLM, dispatch tools, repeat until done."""
    if messages is None:
        messages = []
    messages.append({"role": "user", "content": [{"text": user_message}]})

    while True:
        response = client.converse(
            modelId=CLAUDE_SONNET,
            system=[{"text": SYSTEM_PROMPT}],
            messages=messages,
            toolConfig={"tools": ALL_TOOLS},
        )

        assistant_message = response["output"]["message"]
        messages.append(assistant_message)
        stop_reason = response["stopReason"]

        if stop_reason == "end_turn":
            return extract_text(assistant_message), messages

        if stop_reason == "tool_use":
            tool_results = []
            for block in assistant_message["content"]:
                if "toolUse" in block:
                    tool_name = block["toolUse"]["name"]
                    tool_input = block["toolUse"]["input"]
                    tool_id = block["toolUse"]["toolUseId"]

                    print(f"  [Tool Call] {tool_name}({json.dumps(tool_input)})")
                    result = TOOL_DISPATCH[tool_name](**tool_input)
                    print(f"  [Tool Result] {result[:150]}")

                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_id,
                            "content": [{"text": str(result)}],
                        }
                    })

            messages.append({"role": "user", "content": tool_results})


def chat():
    """Interactive chat with the agent."""
    client = get_client()
    messages = []
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("> ")
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        response, messages = run_agent(client, user_input, messages)
        print(f"\nAgent: {response}\n")


if __name__ == "__main__":
    client = get_client()

    print("=== Single Query ===")
    response, _ = run_agent(
        client,
        "What's the weather in London and are there any recent news about banking regulations?"
    )
    print(f"\nAgent: {response}")

    # Uncomment for interactive chat:
    # print("\n=== Interactive Chat (type 'quit' to exit) ===")
    # chat()
