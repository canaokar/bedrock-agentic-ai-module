"""
Lab 04: Build a Receptionist
Intent-classifying receptionist that routes to specialist agents.
"""

import boto3

import json

CLAUDE_SONNET = "us.anthropic.claude-sonnet-4-20250514"
CLAUDE_HAIKU = "us.anthropic.claude-haiku-4-20250514"
REGION = "ap-south-1"

CONFIDENCE_THRESHOLD = 0.7


def get_client():
    return boto3.client("bedrock-runtime", region_name=REGION)


def extract_text(msg):
    for b in msg.get("content", []):
        if "text" in b:
            return b["text"]
    return ""


# TODO 1: Define intent categories with descriptions
# Create a dict mapping intent names to their descriptions.
# Include at least: faq, account_query, payment_help, tech_support, general
# Example: {"faq": "General questions about services, hours, policies", ...}
INTENT_CATEGORIES = ...


# TODO 2: Write the classifier system prompt
# Instruct Haiku to analyze the user message and return ONLY a JSON object:
# {"intent": "one of the intent names", "confidence": 0.0-1.0, "entities": {...}}
# Hint: List the available intents and their descriptions in the prompt.
CLASSIFIER_PROMPT = ...


def classify_intent(client, user_message):
    """Classify user intent using Claude Haiku (fast and cheap).

    Args:
        client: boto3 bedrock-runtime client.
        user_message: The user's message to classify.

    Returns:
        Dict with keys: intent, confidence, entities.
    """
    # TODO 3: Call Bedrock with CLAUDE_HAIKU and CLASSIFIER_PROMPT
    # Parse the JSON response. Handle JSON parse errors with a fallback.
    # Hint:
    #   response = client.converse(
    #       modelId=CLAUDE_HAIKU,
    #       system=[{"text": CLASSIFIER_PROMPT}],
    #       messages=[{"role": "user", "content": [{"text": user_message}]}],
    #   )
    #   text = extract_text(response["output"]["message"])
    #   return json.loads(text)
    ...


def route_to_specialist(client, intent, user_message):
    """Route the classified message to the appropriate specialist handler.

    Args:
        client: boto3 bedrock-runtime client.
        intent: The classified intent string.
        user_message: The user's original message.

    Returns:
        The specialist's response text.
    """
    # TODO 4: Import specialist handlers from specialists.py
    # from specialists import handle_faq, handle_account, handle_payment, handle_general
    ...

    # TODO 5: Create a mapping from intent to handler and call the right one
    # Hint:
    #   handlers = {
    #       "faq": handle_faq,
    #       "account_query": handle_account,
    #       "payment_help": handle_payment,
    #       "general": handle_general,
    #   }
    #   handler = handlers.get(intent, handle_general)
    #   return handler(user_message)
    ...


def receptionist(user_message):
    """The main receptionist function: classify, route, and respond.

    Args:
        user_message: The user's message.

    Returns:
        The response text.
    """
    client = get_client()

    # Classify
    classification = classify_intent(client, user_message)
    intent = classification.get("intent", "general")
    confidence = classification.get("confidence", 0.0)
    entities = classification.get("entities", {})

    print(f"  Intent: {intent} (confidence: {confidence:.2f})")
    if entities:
        print(f"  Entities: {entities}")

    # TODO 6: Add fallback logic
    # If confidence < CONFIDENCE_THRESHOLD, return a clarification question
    # instead of routing to a specialist.
    # Hint: return "I'm not quite sure what you need. Could you rephrase your question?"
    ...

    # Route to specialist
    return route_to_specialist(client, intent, user_message)


def chat():
    """Interactive receptionist chat loop.

    Maintains conversation context across turns.
    """
    # TODO 7: Implement multi-turn chat
    # Maintain a dict of conversation histories per specialist.
    # On each turn: classify, route, track which specialist was used.
    # Hint:
    #   histories = {}  # {intent: [messages]}
    #   while True:
    #       user_input = input("> ")
    #       response = receptionist(user_input)
    #       print(f"Agent: {response}")
    ...


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
