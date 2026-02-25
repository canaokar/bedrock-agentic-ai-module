"""
Hackathon Building Block: LangGraph Agent Template
A minimal LangGraph StateGraph agent with Bedrock.
Customize the state, nodes, and edges for your use case.

Based on Lab 05a.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
import boto3

import json

CLAUDE_SONNET = "global.anthropic.claude-sonnet-4-6"
CLAUDE_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
REGION = "ap-south-1"

client = boto3.client("bedrock-runtime", region_name=REGION)


def extract_text(message):
    for block in message.get("content", []):
        if "text" in block:
            return block["text"]
    return ""


def call_bedrock(model_id, system_prompt, user_message):
    response = client.converse(
        modelId=model_id,
        system=[{"text": system_prompt}],
        messages=[{"role": "user", "content": [{"text": user_message}]}],
    )
    return extract_text(response["output"]["message"])


# --- Customize your state ---
class AgentState(TypedDict):
    user_input: str
    category: str
    response: str


# --- Customize your nodes ---
def classifier_node(state: AgentState) -> AgentState:
    """Classify the user input into a category."""
    result = call_bedrock(
        CLAUDE_HAIKU,
        'Classify the input into one of: greeting, question, task. Return ONLY the category word.',
        state["user_input"],
    )
    state["category"] = result.strip().lower()
    print(f"  [Classifier] Category: {state['category']}")
    return state


def handler_node(state: AgentState) -> AgentState:
    """Handle the classified input."""
    state["response"] = call_bedrock(
        CLAUDE_SONNET,
        f"You are handling a '{state['category']}' type input. Respond helpfully.",
        state["user_input"],
    )
    return state


def route(state: AgentState) -> Literal["handler", "handler"]:
    """Route based on category. Customize for multiple paths."""
    return "handler"


# --- Build the graph ---
graph = StateGraph(AgentState)
graph.add_node("classify", classifier_node)
graph.add_node("handler", handler_node)
graph.set_entry_point("classify")
graph.add_conditional_edges("classify", route)
graph.add_edge("handler", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"user_input": "What are the key AML requirements?", "category": "", "response": ""})
    print(f"\nResponse: {result['response'][:300]}")
