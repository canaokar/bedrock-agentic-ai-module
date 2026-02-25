"""
Lab 05a: LangGraph Agent — Receptionist as a StateGraph
========================================================
Convert the Lab 04 receptionist into a LangGraph StateGraph so that
routing, specialist dispatch, and (optionally) human-in-the-loop are
all expressed as graph nodes and edges.

Run:
    pip install -r requirements.txt
    python main.py
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
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

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CLAUDE_SONNET = "global.anthropic.claude-sonnet-4-6"
CLAUDE_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
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


# ===================================================================
# TODO 1 — Define AgentState
# ===================================================================
# Create a TypedDict called AgentState with four keys:
#   messages    : list          — conversation history
#   current_intent : str        — classified intent label
#   confidence  : float         — classifier confidence score
#   response    : str           — final answer to return
# -------------------------------------------------------------------

...  # <-- replace with your TypedDict


# ===================================================================
# TODO 2 — Classifier node
# ===================================================================
# Define classifier_node(state: AgentState) -> dict
#   1. Get the latest user message from state["messages"]
#   2. Call Bedrock with CLAUDE_HAIKU and CLASSIFIER_SYSTEM_PROMPT
#   3. Parse the JSON response to extract intent and confidence
#   4. Return a dict with current_intent and confidence keys
# -------------------------------------------------------------------

def classifier_node(state):
    ...  # <-- implement


# ===================================================================
# TODO 3 — Specialist nodes
# ===================================================================
# Create four functions, each with signature  node(state) -> dict
# Each should:
#   1. Get the latest user message from state["messages"]
#   2. Call Bedrock with CLAUDE_SONNET and the appropriate system prompt
#   3. Return {"response": <the model's answer>}
# -------------------------------------------------------------------

def faq_node(state):
    ...  # <-- implement

def account_node(state):
    ...  # <-- implement

def payment_node(state):
    ...  # <-- implement

def general_node(state):
    ...  # <-- implement


# ===================================================================
# TODO 4 — Routing function
# ===================================================================
# Define route_by_intent(state: AgentState) -> str
#   Return the node name that matches state["current_intent"].
#   If confidence < 0.6, fall back to "general".
#   Valid return values: "faq", "account", "payment", "general"
# -------------------------------------------------------------------

def route_by_intent(state):
    ...  # <-- implement


# ===================================================================
# TODO 5 — Build the StateGraph & add nodes
# ===================================================================
# 1. Create  graph = StateGraph(AgentState)
# 2. Add nodes: "classify", "faq", "account", "payment", "general"
# 3. Set entry point to "classify"
# -------------------------------------------------------------------

...  # <-- build graph and add nodes


# ===================================================================
# TODO 6 — Add edges & compile
# ===================================================================
# 1. Add conditional_edges from "classify" using route_by_intent
#    with the mapping {"faq": "faq", "account": "account",
#                       "payment": "payment", "general": "general"}
# 2. Add normal edges from each specialist node to END
# 3. Compile:  app = graph.compile()
# -------------------------------------------------------------------

...  # <-- add edges and compile


# ===================================================================
# TODO 7 (BONUS) — Human-in-the-loop
# ===================================================================
# Re-compile the graph with interrupt_before=["account", "payment"]
# so that sensitive operations pause for human approval.
#
# app_with_hitl = graph.compile(interrupt_before=["account", "payment"])
# -------------------------------------------------------------------

# ...  # <-- uncomment and try


# ===================================================================
# TODO 8 (BONUS) — Feedback loop
# ===================================================================
# Add a "feedback" node after each specialist that asks the user
# whether the answer was helpful. If not, route back to "classify"
# with an updated message. This creates a cycle in the graph.
# -------------------------------------------------------------------

# ...  # <-- design and implement


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
