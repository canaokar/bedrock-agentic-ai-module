"""
Lab 01: Hello Bedrock
Get comfortable with the AWS Bedrock Converse API by making your first LLM calls.
"""

import boto3
import json
import time
import os
from pathlib import Path

# Load .env file if it exists (so you don't have to export every time)
# Looks in: current dir, parent dir, lab dir, shared dir
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

# Model IDs for AWS Bedrock
CLAUDE_SONNET = "global.anthropic.claude-sonnet-4-6"
CLAUDE_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"

REGION = "ap-south-1"


def get_bedrock_client():
    """Create and return a boto3 Bedrock runtime client.

    Returns:
        A boto3 client for the bedrock-runtime service.
    """
    # TODO 1: Create and return a boto3 bedrock-runtime client
    # Hint: boto3.client("bedrock-runtime", region_name=REGION)
    ...


def call_converse(client, model_id, system_prompt, user_message):
    """Call the Bedrock Converse API with a system prompt and user message.

    Args:
        client: boto3 bedrock-runtime client.
        model_id: The model to use (e.g., CLAUDE_SONNET).
        system_prompt: Instructions for the model.
        user_message: The user's question or prompt.

    Returns:
        The response text string from the model.
    """
    # TODO 2: Call client.converse() with the correct message structure
    # Hint:
    #   response = client.converse(
    #       modelId=model_id,
    #       system=[{"text": system_prompt}],
    #       messages=[{"role": "user", "content": [{"text": user_message}]}],
    #   )
    ...

    # TODO 3: Extract and return the response text
    # Hint: response["output"]["message"]["content"][0]["text"]
    ...


def compare_models(client, system_prompt, user_message):
    """Call the same prompt with Sonnet and Haiku, comparing speed and output.

    Args:
        client: boto3 bedrock-runtime client.
        system_prompt: Instructions for the model.
        user_message: The user's question.
    """
    # TODO 4: Call with Claude Sonnet, then Claude Haiku
    # Time each call with time.time() and print the model name, duration, and response.
    # Hint:
    #   start = time.time()
    #   response = call_converse(client, CLAUDE_SONNET, system_prompt, user_message)
    #   print(f"Sonnet ({time.time() - start:.1f}s): {response[:200]}")
    #   ... repeat for Haiku ...
    ...


def chat_loop(client, model_id, system_prompt):
    """Run an interactive chat loop maintaining conversation history.

    Args:
        client: boto3 bedrock-runtime client.
        model_id: The model to use.
        system_prompt: Instructions for the model.
    """
    messages = []

    # TODO 5: Implement the chat loop
    # 1. while True: get user input with input("> ")
    # 2. Break on "quit" or "exit"
    # 3. Append {"role": "user", "content": [{"text": user_input}]} to messages
    # 4. Call client.converse(modelId=model_id, system=[{"text": system_prompt}], messages=messages)
    # 5. Extract assistant response text
    # 6. Append assistant message to messages: {"role": "assistant", "content": [{"text": response}]}
    # 7. Print the response
    ...


def stream_response(client, model_id, system_prompt, user_message):
    """Call Bedrock with streaming and print tokens as they arrive.

    Args:
        client: boto3 bedrock-runtime client.
        model_id: The model to use.
        system_prompt: Instructions for the model.
        user_message: The user's question.
    """
    # TODO 6 (BONUS): Implement streaming with converse_stream()
    # Hint:
    #   response = client.converse_stream(
    #       modelId=model_id,
    #       system=[{"text": system_prompt}],
    #       messages=[{"role": "user", "content": [{"text": user_message}]}],
    #   )
    #   for event in response["stream"]:
    #       if "contentBlockDelta" in event:
    #           print(event["contentBlockDelta"]["delta"]["text"], end="", flush=True)
    ...


if __name__ == "__main__":
    SYSTEM_PROMPT = "You are a helpful banking compliance assistant. Be concise."

    client = get_bedrock_client()

    # Test basic call
    print("=== Basic Converse Call ===")
    response = call_converse(
        client, CLAUDE_SONNET, SYSTEM_PROMPT,
        "What are the key components of an AML compliance program?"
    )
    print(f"Response:\n{response}\n")

    # Compare models
    print("=== Model Comparison ===")
    compare_models(
        client, SYSTEM_PROMPT,
        "Summarize KYC requirements in one paragraph."
    )

    # Uncomment to test chat loop:
    # print("\n=== Interactive Chat (type 'quit' to exit) ===")
    # chat_loop(client, CLAUDE_SONNET, SYSTEM_PROMPT)

    # Uncomment to test streaming:
    # print("\n=== Streaming Response ===")
    # stream_response(client, CLAUDE_SONNET, SYSTEM_PROMPT, "What is PEP screening?")
