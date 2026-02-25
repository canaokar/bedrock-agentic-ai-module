"""
Lab 01: Hello Bedrock (Solution)
"""

import boto3
import json
import time
import os
from pathlib import Path

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


def get_bedrock_client():
    """Create and return a boto3 Bedrock runtime client."""
    return boto3.client("bedrock-runtime", region_name=REGION)


def call_converse(client, model_id, system_prompt, user_message):
    """Call the Bedrock Converse API with a system prompt and user message."""
    response = client.converse(
        modelId=model_id,
        system=[{"text": system_prompt}],
        messages=[{"role": "user", "content": [{"text": user_message}]}],
    )
    return response["output"]["message"]["content"][0]["text"]


def compare_models(client, system_prompt, user_message):
    """Call the same prompt with Sonnet and Haiku, comparing speed and output."""
    print(f"Prompt: {user_message}\n")

    start = time.time()
    sonnet_response = call_converse(client, CLAUDE_SONNET, system_prompt, user_message)
    sonnet_time = time.time() - start
    print(f"Sonnet ({sonnet_time:.1f}s):\n{sonnet_response}\n")

    start = time.time()
    haiku_response = call_converse(client, CLAUDE_HAIKU, system_prompt, user_message)
    haiku_time = time.time() - start
    print(f"Haiku ({haiku_time:.1f}s):\n{haiku_response}\n")

    print(f"Speed difference: Haiku was {sonnet_time/haiku_time:.1f}x faster")


def chat_loop(client, model_id, system_prompt):
    """Run an interactive chat loop maintaining conversation history."""
    messages = []
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("> ")
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": [{"text": user_input}]})

        response = client.converse(
            modelId=model_id,
            system=[{"text": system_prompt}],
            messages=messages,
        )

        assistant_text = response["output"]["message"]["content"][0]["text"]
        messages.append({"role": "assistant", "content": [{"text": assistant_text}]})

        print(f"\nAssistant: {assistant_text}\n")


def stream_response(client, model_id, system_prompt, user_message):
    """Call Bedrock with streaming and print tokens as they arrive."""
    response = client.converse_stream(
        modelId=model_id,
        system=[{"text": system_prompt}],
        messages=[{"role": "user", "content": [{"text": user_message}]}],
    )

    print("Streaming: ", end="")
    for event in response["stream"]:
        if "contentBlockDelta" in event:
            text = event["contentBlockDelta"]["delta"]["text"]
            print(text, end="", flush=True)
    print("\n")


if __name__ == "__main__":
    SYSTEM_PROMPT = "You are a helpful banking compliance assistant. Be concise."

    client = get_bedrock_client()

    print("=== Basic Converse Call ===")
    response = call_converse(
        client, CLAUDE_SONNET, SYSTEM_PROMPT,
        "What are the key components of an AML compliance program?"
    )
    print(f"Response:\n{response}\n")

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
