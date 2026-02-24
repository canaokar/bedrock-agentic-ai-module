"""
Shared Bedrock client utilities for all Agentic AI labs.
Provides a simplified interface to the AWS Bedrock Converse API.

Authentication: export AWS_BEARER_TOKEN_BEDROCK in your terminal.
boto3 picks it up automatically.
"""

import boto3
import json
import time

# ---------------------------------------------------------------------------
# Model ID constants — update these if newer model versions become available
# ---------------------------------------------------------------------------
CLAUDE_SONNET = "global.anthropic.claude-sonnet-4-6"
CLAUDE_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
LLAMA = "meta.llama3-8b-instruct-v1:0"

REGION = "ap-south-1"


def get_bedrock_client(region=REGION):
    """Create and return a boto3 Bedrock runtime client.

    Authentication is via the AWS_BEARER_TOKEN_BEDROCK environment variable.
    Export it in your terminal before running any lab.
    """
    return boto3.client("bedrock-runtime", region_name=region)


def converse(client, model_id, messages, system_prompt=None, tools=None):
    """Simplified wrapper around client.converse().

    Args:
        client: boto3 bedrock-runtime client.
        model_id: Bedrock model identifier.
        messages: List of message dicts (role + content).
        system_prompt: Optional system instruction string.
        tools: Optional list of tool schemas.

    Returns:
        Tuple of (assistant_message_dict, stop_reason_string).
    """
    kwargs = {"modelId": model_id, "messages": messages}
    if system_prompt:
        kwargs["system"] = [{"text": system_prompt}]
    if tools:
        kwargs["toolConfig"] = {"tools": tools}

    response = client.converse(**kwargs)
    return response["output"]["message"], response["stopReason"]


def converse_with_tools(client, model_id, system_prompt, tools, tool_dispatch,
                        user_message, messages=None, verbose=False):
    """Run a complete agent loop: call LLM, dispatch tools, repeat until done.

    Args:
        client: boto3 bedrock-runtime client.
        model_id: Bedrock model identifier.
        system_prompt: System instruction string.
        tools: List of tool schemas for toolConfig.
        tool_dispatch: Dict mapping tool name to callable.
        user_message: The user's initial message string.
        messages: Optional existing message history (will be mutated).
        verbose: If True, print each tool call for debugging.

    Returns:
        Tuple of (final_text_response, full_messages_list).
    """
    if messages is None:
        messages = []
    messages.append({"role": "user", "content": [{"text": user_message}]})

    while True:
        response = client.converse(
            modelId=model_id,
            system=[{"text": system_prompt}],
            messages=messages,
            toolConfig={"tools": tools},
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

                    if verbose:
                        print(f"  -> Calling {tool_name}({json.dumps(tool_input)})")

                    try:
                        result = tool_dispatch[tool_name](**tool_input)
                    except Exception as e:
                        result = json.dumps({"error": str(e)})

                    if verbose:
                        print(f"  <- {result[:200]}")

                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_id,
                            "content": [{"text": str(result)}],
                        }
                    })

            messages.append({"role": "user", "content": tool_results})


def extract_text(message):
    """Extract the first text block from a Bedrock response message.

    Args:
        message: The assistant message dict from a Converse response.

    Returns:
        The text string, or empty string if no text block found.
    """
    for block in message.get("content", []):
        if "text" in block:
            return block["text"]
    return ""
