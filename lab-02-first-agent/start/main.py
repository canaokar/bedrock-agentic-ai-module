"""
Lab 02: Build Your First Agent
Build a tool-using agent from scratch with the Bedrock Converse API agent loop.
"""

import boto3

import json
from tools import ALL_TOOLS, TOOL_DISPATCH

CLAUDE_SONNET = "us.anthropic.claude-sonnet-4-20250514"
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
    """Run the agent loop: call LLM, dispatch tools, repeat until done.

    Args:
        client: boto3 bedrock-runtime client.
        user_message: The user's message string.
        messages: Optional existing conversation history.

    Returns:
        Tuple of (response_text, messages_list).
    """
    if messages is None:
        messages = []
    messages.append({"role": "user", "content": [{"text": user_message}]})

    # TODO 5: Call the Converse API with toolConfig
    # Hint:
    #   response = client.converse(
    #       modelId=CLAUDE_SONNET,
    #       system=[{"text": SYSTEM_PROMPT}],
    #       messages=messages,
    #       toolConfig={"tools": ALL_TOOLS},
    #   )
    ...

    # TODO 6: Implement the agent loop
    # The loop should:
    # 1. Get the assistant message from response["output"]["message"]
    # 2. Append it to messages
    # 3. Check response["stopReason"]:
    #    - If "end_turn": extract text and return (response_text, messages)
    #    - If "tool_use": for each block in assistant message content:
    #        a. Check if block has "toolUse" key
    #        b. Extract: tool_name = block["toolUse"]["name"]
    #                    tool_input = block["toolUse"]["input"]
    #                    tool_id = block["toolUse"]["toolUseId"]
    #        c. Call: result = TOOL_DISPATCH[tool_name](**tool_input)
    #        d. Build toolResult: {"toolResult": {"toolUseId": tool_id, "content": [{"text": str(result)}]}}
    #    - Append tool results as: messages.append({"role": "user", "content": tool_results_list})
    #    - Call converse() again with updated messages
    #    - Repeat until "end_turn"
    ...


def chat():
    """Interactive chat with the agent.

    Maintains conversation history across turns.
    """
    # TODO 7: Implement an interactive chat loop
    # 1. Create the client and an empty messages list
    # 2. Loop: get user input, call run_agent with the shared messages list
    # 3. Print the response
    # 4. Break on "quit" or "exit"
    ...


if __name__ == "__main__":
    client = get_client()

    # Single query test
    print("=== Single Query ===")
    response, _ = run_agent(
        client,
        "What's the weather in London and are there any recent news about banking regulations?"
    )
    print(f"\nAgent: {response}")

    # Uncomment for interactive chat:
    # print("\n=== Interactive Chat (type 'quit' to exit) ===")
    # chat()
