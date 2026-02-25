"""
Lab 04: Specialist agent handlers (Solution).
"""

import boto3
import os
from pathlib import Path

import json

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


# ═══ FAQ Specialist ═══

FAQ_SYSTEM_PROMPT = "You are an FAQ specialist for a banking service. Answer common questions using the search_faq tool. Be concise and friendly."

FAQ_TOOL = {"toolSpec": {"name": "search_faq", "description": "Search the FAQ knowledge base.", "inputSchema": {"json": {"type": "object", "properties": {"question": {"type": "string"}}, "required": ["question"]}}}}

def search_faq(question):
    faqs = {
        "hours": "Branches are open Monday-Friday 9am-5pm. Some offer Saturday 9am-1pm.",
        "opening": "Branches are open Monday-Friday 9am-5pm. Some offer Saturday 9am-1pm.",
        "card": "Report lost/stolen card: call 0800-XXX-XXXX or freeze in the mobile app.",
        "lost": "Report lost/stolen card: call 0800-XXX-XXXX or freeze in the mobile app.",
        "overdraft": "Standard overdraft up to 1,000. Premium accounts may get more.",
        "savings": "We offer easy-access savings, fixed-rate ISAs, and regular saver accounts.",
        "close": "Close your account online, by phone, or in branch. Move direct debits first.",
    }
    for key, answer in faqs.items():
        if key in question.lower():
            return json.dumps({"found": True, "answer": answer})
    return json.dumps({"found": False, "answer": "No specific FAQ found. Contact customer service."})

def handle_faq(user_message):
    return _run_specialist(FAQ_SYSTEM_PROMPT, [FAQ_TOOL], {"search_faq": search_faq}, user_message)


# ═══ Account Specialist ═══

ACCOUNT_SYSTEM_PROMPT = "You are an account specialist. Help customers check balances, view transactions, and manage account settings. Use available tools."

BALANCE_TOOL = {"toolSpec": {"name": "check_balance", "description": "Check account balance.", "inputSchema": {"json": {"type": "object", "properties": {"account_id": {"type": "string", "description": "Account ID (default: main account)"}}, "required": []}}}}
TRANSACTIONS_TOOL = {"toolSpec": {"name": "get_transactions", "description": "Get recent transactions.", "inputSchema": {"json": {"type": "object", "properties": {"account_id": {"type": "string"}, "limit": {"type": "integer", "description": "Number of transactions (default 5)"}}, "required": []}}}}

def check_balance(account_id="main"):
    return json.dumps({"account_id": account_id, "balance": 2847.50, "currency": "GBP", "available": 2347.50, "overdraft_limit": 500.00})

def get_transactions(account_id="main", limit=5):
    txns = [
        {"date": "2025-01-20", "description": "Tesco Supermarket", "amount": -45.30},
        {"date": "2025-01-19", "description": "Salary - NatWest Group", "amount": 3200.00},
        {"date": "2025-01-18", "description": "Netflix", "amount": -15.99},
        {"date": "2025-01-17", "description": "ATM Withdrawal", "amount": -100.00},
        {"date": "2025-01-16", "description": "Costa Coffee", "amount": -4.50},
    ]
    return json.dumps({"transactions": txns[:limit]})

def handle_account(user_message):
    return _run_specialist(ACCOUNT_SYSTEM_PROMPT, [BALANCE_TOOL, TRANSACTIONS_TOOL], {"check_balance": check_balance, "get_transactions": get_transactions}, user_message)


# ═══ Payment Specialist ═══

PAYMENT_SYSTEM_PROMPT = "You are a payment specialist. Help customers with transfers, payment status, and standing orders. Use available tools."

PAYMENT_STATUS_TOOL = {"toolSpec": {"name": "check_payment_status", "description": "Check status of a payment.", "inputSchema": {"json": {"type": "object", "properties": {"reference": {"type": "string"}}, "required": []}}}}
TRANSFER_TOOL = {"toolSpec": {"name": "initiate_transfer", "description": "Initiate a bank transfer.", "inputSchema": {"json": {"type": "object", "properties": {"to_account": {"type": "string"}, "amount": {"type": "number"}}, "required": ["to_account", "amount"]}}}}

def check_payment_status(reference="latest"):
    return json.dumps({"reference": reference, "status": "completed", "amount": 250.00, "date": "2025-01-19"})

def initiate_transfer(to_account, amount):
    return json.dumps({"status": "initiated", "to_account": to_account, "amount": amount, "reference": "TXN-2025-0042", "estimated_arrival": "same day"})

def handle_payment(user_message):
    return _run_specialist(PAYMENT_SYSTEM_PROMPT, [PAYMENT_STATUS_TOOL, TRANSFER_TOOL], {"check_payment_status": check_payment_status, "initiate_transfer": initiate_transfer}, user_message)


# ═══ General Specialist ═══

def handle_general(user_message):
    client = _get_client()
    response = client.converse(
        modelId=CLAUDE_SONNET,
        system=[{"text": "You are a friendly banking assistant. If you can't help with something, suggest the customer contact their branch."}],
        messages=[{"role": "user", "content": [{"text": user_message}]}],
    )
    return _extract_text(response["output"]["message"])
