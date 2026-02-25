"""
Lab 04: Build a Receptionist (Solution)
"""

import boto3
import os
from pathlib import Path

import json
from specialists import handle_faq, handle_account, handle_payment, handle_general

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

CONFIDENCE_THRESHOLD = 0.7

client = boto3.client("bedrock-runtime", region_name=REGION)


def extract_text(msg):
    for b in msg.get("content", []):
        if "text" in b:
            return b["text"]
    return ""


INTENT_CATEGORIES = {
    "faq": "General questions about services, hours, policies, products",
    "account_query": "Account balance, transactions, settings, personal details",
    "payment_help": "Transfers, payments, standing orders, direct debits",
    "tech_support": "Login issues, app problems, online banking technical help",
    "general": "Anything that does not fit the other categories",
}

CLASSIFIER_PROMPT = f"""You are an intent classifier for a banking chatbot.

Available intents:
{json.dumps(INTENT_CATEGORIES, indent=2)}

Analyze the user message and respond with ONLY a JSON object:
{{"intent": "one of the intent names above", "confidence": 0.0 to 1.0, "entities": {{}}}}

Rules:
- Choose the most specific intent that matches
- Set confidence based on how clearly the message matches
- Extract relevant entities (amounts, account types, etc.)"""


def classify_intent(user_message):
    response = client.converse(
        modelId=CLAUDE_HAIKU,
        system=[{"text": CLASSIFIER_PROMPT}],
        messages=[{"role": "user", "content": [{"text": user_message}]}],
    )
    text = extract_text(response["output"]["message"])
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"intent": "general", "confidence": 0.5, "entities": {}}


HANDLERS = {
    "faq": handle_faq,
    "account_query": handle_account,
    "payment_help": handle_payment,
    "tech_support": handle_general,
    "general": handle_general,
}


def receptionist(user_message):
    classification = classify_intent(user_message)
    intent = classification.get("intent", "general")
    confidence = classification.get("confidence", 0.0)
    entities = classification.get("entities", {})

    print(f"  Intent: {intent} (confidence: {confidence:.2f})")
    if entities:
        print(f"  Entities: {entities}")

    if confidence < CONFIDENCE_THRESHOLD:
        return "I'm not quite sure what you need. Could you rephrase your question or provide more details?"

    handler = HANDLERS.get(intent, handle_general)
    return handler(user_message)


def chat():
    print("Banking Receptionist (type 'quit' to exit)\n")
    while True:
        user_input = input("> ")
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        print()
        response = receptionist(user_input)
        print(f"\nAgent: {response}\n")


if __name__ == "__main__":
    test_queries = [
        "What are your opening hours?",
        "What's my account balance?",
        "I want to transfer 500 pounds to my savings",
        "Tell me a joke",
    ]

    for query in test_queries:
        print(f"\nUser: {query}")
        response = receptionist(query)
        print(f"Agent: {response[:250]}")
        print("-" * 50)
