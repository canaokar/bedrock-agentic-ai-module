"""
Lab 04: Specialist agent handlers.
Each specialist handles a specific intent with its own tools and system prompt.
"""

import boto3

import json

CLAUDE_SONNET = "global.anthropic.claude-sonnet-4-6"
REGION = "ap-south-1"

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = boto3.client("bedrock-runtime", region_name=REGION)
    return _client

def _extract_text(msg):
    for b in msg.get("content", []):
        if "text" in b:
            return b["text"]
    return ""

def _run_specialist(system_prompt, tools, tool_dispatch, user_message):
    """Run a specialist agent with optional tools."""
    client = _get_client()
    messages = [{"role": "user", "content": [{"text": user_message}]}]

    while True:
        kwargs = {"modelId": CLAUDE_SONNET, "system": [{"text": system_prompt}], "messages": messages}
        if tools:
            kwargs["toolConfig"] = {"tools": tools}
        response = client.converse(**kwargs)
        msg = response["output"]["message"]
        messages.append(msg)

        if response["stopReason"] == "end_turn":
            return _extract_text(msg)

        if response["stopReason"] == "tool_use":
            results = []
            for b in msg["content"]:
                if "toolUse" in b:
                    name, inp, tid = b["toolUse"]["name"], b["toolUse"]["input"], b["toolUse"]["toolUseId"]
                    try:
                        out = tool_dispatch[name](**inp)
                    except Exception as e:
                        out = json.dumps({"error": str(e)})
                    results.append({"toolResult": {"toolUseId": tid, "content": [{"text": str(out)}]}})
            messages.append({"role": "user", "content": results})


# ═══════════════════════════════════════════════════════════════════
# FAQ Specialist — PROVIDED COMPLETE as a reference pattern
# ═══════════════════════════════════════════════════════════════════

FAQ_SYSTEM_PROMPT = """You are an FAQ specialist for a banking service.
Answer common questions using the search_faq tool.
Be concise, friendly, and accurate."""

FAQ_TOOL = {
    "toolSpec": {
        "name": "search_faq",
        "description": "Search the FAQ knowledge base.",
        "inputSchema": {"json": {"type": "object", "properties": {"question": {"type": "string"}}, "required": ["question"]}}
    }
}

def search_faq(question):
    """Mock FAQ search with realistic banking FAQ data."""
    faqs = {
        "hours": "Branches are open Monday-Friday 9am-5pm. Some branches offer Saturday 9am-1pm.",
        "opening": "Branches are open Monday-Friday 9am-5pm. Some branches offer Saturday 9am-1pm.",
        "card": "Report a lost/stolen card immediately: call 0800-XXX-XXXX or freeze it in the mobile app.",
        "lost": "Report a lost/stolen card immediately: call 0800-XXX-XXXX or freeze it in the mobile app.",
        "overdraft": "Standard overdraft limit is up to 1,000. Premium accounts may qualify for higher limits.",
        "atm": "Daily ATM withdrawal limit is 300 (500 for premium accounts).",
        "close": "Close your account online, by phone, or in branch. Move direct debits first.",
        "savings": "We offer easy-access savings, fixed-rate ISAs, and regular saver accounts.",
    }
    for key, answer in faqs.items():
        if key in question.lower():
            return json.dumps({"found": True, "answer": answer})
    return json.dumps({"found": False, "answer": "No specific FAQ found. Please contact customer service."})


def handle_faq(user_message):
    """Handle FAQ-classified messages."""
    return _run_specialist(FAQ_SYSTEM_PROMPT, [FAQ_TOOL], {"search_faq": search_faq}, user_message)


# ═══════════════════════════════════════════════════════════════════
# Account Specialist
# ═══════════════════════════════════════════════════════════════════

# TODO: Define ACCOUNT_SYSTEM_PROMPT
# Hint: "You are an account specialist. Help customers with balance inquiries,
#        transaction history, and account settings."
ACCOUNT_SYSTEM_PROMPT = ...

# TODO: Define account tools — check_balance(account_id) and get_transactions(account_id, limit)
BALANCE_TOOL = ...
TRANSACTIONS_TOOL = ...

def check_balance(account_id="default"):
    """Mock balance check."""
    # TODO: Return mock balance data as JSON
    # Hint: return json.dumps({"account_id": account_id, "balance": 2847.50, "currency": "GBP"})
    ...

def get_transactions(account_id="default", limit=5):
    """Mock transaction history."""
    # TODO: Return mock transactions as JSON
    # Hint: Return a list of 3-5 mock transactions with date, description, amount
    ...

def handle_account(user_message):
    """Handle account query messages."""
    # TODO: Wire up using _run_specialist with ACCOUNT_SYSTEM_PROMPT and account tools
    ...


# ═══════════════════════════════════════════════════════════════════
# Payment Specialist
# ═══════════════════════════════════════════════════════════════════

# TODO: Define PAYMENT_SYSTEM_PROMPT
PAYMENT_SYSTEM_PROMPT = ...

# TODO: Define payment tools — check_payment_status(reference) and initiate_transfer(to_account, amount)
PAYMENT_STATUS_TOOL = ...
TRANSFER_TOOL = ...

def check_payment_status(reference="default"):
    """Mock payment status check."""
    # TODO: Return mock payment status
    ...

def initiate_transfer(to_account, amount):
    """Mock transfer initiation."""
    # TODO: Return mock transfer confirmation
    ...

def handle_payment(user_message):
    """Handle payment-related messages."""
    # TODO: Wire up using _run_specialist
    ...


# ═══════════════════════════════════════════════════════════════════
# General Specialist
# ═══════════════════════════════════════════════════════════════════

def handle_general(user_message):
    """Handle general/unclassified messages with a simple conversational response."""
    # TODO: Implement a simple converse() call with no tools
    # Use a friendly general-purpose system prompt
    ...
