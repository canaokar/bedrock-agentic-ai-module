"""
Lab 05a: LangGraph Agent — Receptionist as a StateGraph (SOLUTION)
===================================================================
Complete working solution with all TODOs implemented.

Run:
    pip install -r ../start/requirements.txt
    python main.py
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
import boto3

import json

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CLAUDE_SONNET = "us.anthropic.claude-sonnet-4-20250514"
CLAUDE_HAIKU = "us.anthropic.claude-haiku-4-20250514"
REGION = "ap-south-1"

bedrock = boto3.client("bedrock-runtime", region_name=REGION)

# ---------------------------------------------------------------------------
# Specialist system prompts
# ---------------------------------------------------------------------------
FAQ_SYSTEM_PROMPT = (
    "You are an FAQ specialist for a retail bank. Answer common questions "
    "about branch hours, card activation, online-banking enrollment, and "
    "general bank policies. Be concise and friendly."
)

ACCOUNT_SYSTEM_PROMPT = (
    "You are an account-services specialist. Help customers with balance "
    "inquiries, opening or closing accounts, updating personal details, "
    "and explaining account types. Always verify you are speaking to the "
    "account holder before sharing sensitive information."
)

PAYMENT_SYSTEM_PROMPT = (
    "You are a payments specialist. Assist customers with money transfers, "
    "bill payments, direct debits, standing orders, and payment disputes. "
    "Provide clear step-by-step instructions."
)

GENERAL_SYSTEM_PROMPT = (
    "You are a friendly general-purpose banking assistant. If the customer's "
    "question does not fit neatly into FAQ, accounts, or payments, do your "
    "best to help or direct them to the right department."
)

CLASSIFIER_SYSTEM_PROMPT = (
    "You are a customer-intent classifier for a retail bank. "
    "Given the customer message, respond with ONLY a JSON object "
    '(no markdown, no explanation) with two keys:\n'
    '  "intent": one of "faq", "account", "payment", "general"\n'
    '  "confidence": a float between 0.0 and 1.0\n'
    "Example: {\"intent\": \"faq\", \"confidence\": 0.92}"
)


# ---------------------------------------------------------------------------
# Helper — call Bedrock Converse API
# ---------------------------------------------------------------------------
def call_bedrock(model_id: str, system_prompt: str, user_message: str) -> str:
    """Send a single-turn message to Bedrock and return the text response."""
    response = bedrock.converse(
        modelId=model_id,
        system=[{"text": system_prompt}],
        messages=[{"role": "user", "content": [{"text": user_message}]}],
    )
    return response["output"]["message"]["content"][0]["text"]


# ---------------------------------------------------------------------------
# TODO 1 — Define AgentState
# ---------------------------------------------------------------------------
class AgentState(TypedDict):
    messages: list
    current_intent: str
    confidence: float
    response: str


# ---------------------------------------------------------------------------
# TODO 2 — Classifier node
# ---------------------------------------------------------------------------
def classifier_node(state: AgentState) -> dict:
    """Classify the customer's intent using Haiku."""
    latest_message = state["messages"][-1]["content"]

    raw = call_bedrock(CLAUDE_HAIKU, CLASSIFIER_SYSTEM_PROMPT, latest_message)

    try:
        parsed = json.loads(raw)
        intent = parsed.get("intent", "general")
        confidence = float(parsed.get("confidence", 0.0))
    except (json.JSONDecodeError, ValueError):
        intent = "general"
        confidence = 0.0

    return {"current_intent": intent, "confidence": confidence}


# ---------------------------------------------------------------------------
# TODO 3 — Specialist nodes
# ---------------------------------------------------------------------------
def faq_node(state: AgentState) -> dict:
    """Handle FAQ queries."""
    latest_message = state["messages"][-1]["content"]
    answer = call_bedrock(CLAUDE_SONNET, FAQ_SYSTEM_PROMPT, latest_message)
    return {"response": answer}


def account_node(state: AgentState) -> dict:
    """Handle account-related queries."""
    latest_message = state["messages"][-1]["content"]
    answer = call_bedrock(CLAUDE_SONNET, ACCOUNT_SYSTEM_PROMPT, latest_message)
    return {"response": answer}


def payment_node(state: AgentState) -> dict:
    """Handle payment-related queries."""
    latest_message = state["messages"][-1]["content"]
    answer = call_bedrock(CLAUDE_SONNET, PAYMENT_SYSTEM_PROMPT, latest_message)
    return {"response": answer}


def general_node(state: AgentState) -> dict:
    """Handle general queries."""
    latest_message = state["messages"][-1]["content"]
    answer = call_bedrock(CLAUDE_SONNET, GENERAL_SYSTEM_PROMPT, latest_message)
    return {"response": answer}


# ---------------------------------------------------------------------------
# TODO 4 — Routing function
# ---------------------------------------------------------------------------
def route_by_intent(state: AgentState) -> str:
    """Route to the appropriate specialist node based on classified intent."""
    if state["confidence"] < 0.6:
        return "general"

    intent = state["current_intent"]
    if intent in ("faq", "account", "payment"):
        return intent
    return "general"


# ---------------------------------------------------------------------------
# TODO 5 — Build the StateGraph & add nodes
# ---------------------------------------------------------------------------
graph = StateGraph(AgentState)

graph.add_node("classify", classifier_node)
graph.add_node("faq", faq_node)
graph.add_node("account", account_node)
graph.add_node("payment", payment_node)
graph.add_node("general", general_node)

graph.set_entry_point("classify")

# ---------------------------------------------------------------------------
# TODO 6 — Add edges & compile
# ---------------------------------------------------------------------------
graph.add_conditional_edges(
    "classify",
    route_by_intent,
    {
        "faq": "faq",
        "account": "account",
        "payment": "payment",
        "general": "general",
    },
)

graph.add_edge("faq", END)
graph.add_edge("account", END)
graph.add_edge("payment", END)
graph.add_edge("general", END)

app = graph.compile()


# ---------------------------------------------------------------------------
# TODO 7 (BONUS) — Human-in-the-loop
# ---------------------------------------------------------------------------
# Uncomment the lines below to enable human-in-the-loop for sensitive nodes.
# This requires a checkpointer (e.g. MemorySaver) to persist state across
# interrupts.
#
# from langgraph.checkpoint.memory import MemorySaver
# memory = MemorySaver()
# app_with_hitl = graph.compile(
#     checkpointer=memory,
#     interrupt_before=["account", "payment"],
# )


# ---------------------------------------------------------------------------
# TODO 8 (BONUS) — Feedback loop
# ---------------------------------------------------------------------------
# To add a feedback loop you would:
# 1. Add a "feedback" node that asks the user if the answer was helpful.
# 2. Add conditional_edges from "feedback" back to "classify" (if unhelpful)
#    or to END (if helpful).
# 3. Replace the specialist -> END edges with specialist -> "feedback".
# This creates a cycle, which LangGraph handles natively.


# ---------------------------------------------------------------------------
# Main — test the graph
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_queries = [
        "What time does the London branch close on Saturdays?",
        "I need to check my current account balance.",
        "How do I set up a standing order to pay my rent?",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Customer: {query}")
        print("=" * 60)

        initial_state = {
            "messages": [{"role": "user", "content": query}],
            "current_intent": "",
            "confidence": 0.0,
            "response": "",
        }

        result = app.invoke(initial_state)

        print(f"Intent   : {result['current_intent']} "
              f"(confidence: {result['confidence']:.2f})")
        print(f"Response : {result['response']}")
