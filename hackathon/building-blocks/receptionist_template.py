"""
Hackathon Building Block: Receptionist Template
Intent classifier + router + specialist handlers.
Copy and customize the intents, specialists, and tools.

Based on Lab 04.
"""

import boto3

import json

CLAUDE_SONNET = "us.anthropic.claude-sonnet-4-20250514"
CLAUDE_HAIKU = "us.anthropic.claude-haiku-4-20250514"
REGION = "ap-south-1"

# --- Customize your intents ---
INTENT_CATEGORIES = {
    "faq": "General questions about services, hours, policies",
    "account": "Account balance, transactions, settings",
    "payment": "Transfers, payments, standing orders",
    "general": "Anything that does not fit other categories",
}

CLASSIFIER_PROMPT = """You are an intent classifier. Analyze the user message and respond with ONLY a JSON object:
{
  "intent": "one of: faq, account, payment, general",
  "confidence": 0.0 to 1.0,
  "entities": {}
}"""

CONFIDENCE_THRESHOLD = 0.7


def get_client():
    return boto3.client("bedrock-runtime", region_name=REGION)


def extract_text(message):
    for block in message.get("content", []):
        if "text" in block:
            return block["text"]
    return ""


def classify_intent(client, user_message):
    """Classify user intent using Haiku (fast/cheap)."""
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


# --- Customize your specialists ---
def handle_faq(client, message):
    response = client.converse(
        modelId=CLAUDE_SONNET,
        system=[{"text": "You are an FAQ specialist. Answer common questions helpfully."}],
        messages=[{"role": "user", "content": [{"text": message}]}],
    )
    return extract_text(response["output"]["message"])


def handle_account(client, message):
    response = client.converse(
        modelId=CLAUDE_SONNET,
        system=[{"text": "You are an account specialist. Help with account queries."}],
        messages=[{"role": "user", "content": [{"text": message}]}],
    )
    return extract_text(response["output"]["message"])


def handle_payment(client, message):
    response = client.converse(
        modelId=CLAUDE_SONNET,
        system=[{"text": "You are a payment specialist. Help with transfers and payments."}],
        messages=[{"role": "user", "content": [{"text": message}]}],
    )
    return extract_text(response["output"]["message"])


def handle_general(client, message):
    response = client.converse(
        modelId=CLAUDE_SONNET,
        system=[{"text": "You are a helpful assistant."}],
        messages=[{"role": "user", "content": [{"text": message}]}],
    )
    return extract_text(response["output"]["message"])


SPECIALIST_MAP = {
    "faq": handle_faq,
    "account": handle_account,
    "payment": handle_payment,
    "general": handle_general,
}


def receptionist(user_message):
    """Classify intent and route to the appropriate specialist."""
    client = get_client()

    classification = classify_intent(client, user_message)
    intent = classification.get("intent", "general")
    confidence = classification.get("confidence", 0)

    print(f"  Intent: {intent} (confidence: {confidence:.2f})")

    if confidence < CONFIDENCE_THRESHOLD:
        return "I'm not quite sure what you need. Could you rephrase your question?"

    handler = SPECIALIST_MAP.get(intent, handle_general)
    return handler(client, user_message)


if __name__ == "__main__":
    queries = [
        "What are your opening hours?",
        "Check my account balance",
        "I want to transfer money",
    ]
    for q in queries:
        print(f"\nUser: {q}")
        response = receptionist(q)
        print(f"Agent: {response[:200]}")
