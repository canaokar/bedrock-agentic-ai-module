"""
Lab 03: Smart Agent (Solution)
"""

import boto3

import json
import time
from datetime import datetime

CLAUDE_SONNET = "global.anthropic.claude-sonnet-4-6"
CLAUDE_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
REGION = "ap-south-1"

client = boto3.client("bedrock-runtime", region_name=REGION)

WEATHER_TOOL = {"toolSpec": {"name": "get_weather", "description": "Get current weather for a city.", "inputSchema": {"json": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}}
NEWS_TOOL = {"toolSpec": {"name": "search_news", "description": "Search recent news on a topic.", "inputSchema": {"json": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}}
TIME_TOOL = {"toolSpec": {"name": "get_time", "description": "Get current time in a timezone.", "inputSchema": {"json": {"type": "object", "properties": {"timezone": {"type": "string"}}, "required": ["timezone"]}}}}
BROKEN_TOOL = {"toolSpec": {"name": "get_stock_price", "description": "Get stock price (may fail).", "inputSchema": {"json": {"type": "object", "properties": {"symbol": {"type": "string"}}, "required": ["symbol"]}}}}

ALL_TOOLS = [WEATHER_TOOL, NEWS_TOOL, TIME_TOOL, BROKEN_TOOL]

def get_weather(city):
    data = {"London": {"temp_c": 12, "condition": "Cloudy"}, "New York": {"temp_c": 22, "condition": "Sunny"}}
    return json.dumps(data.get(city, {"temp_c": 20, "condition": "Unknown"}))

def search_news(query):
    return json.dumps({"headlines": [f"New {query} regulations announced", f"{query} industry update"]})

def get_time(timezone):
    return json.dumps({"timezone": timezone, "time": datetime.now().strftime("%H:%M:%S")})

def get_stock_price(symbol):
    raise ConnectionError(f"Stock API unavailable for {symbol}")

TOOL_DISPATCH = {"get_weather": get_weather, "search_news": search_news, "get_time": get_time, "get_stock_price": get_stock_price}


def extract_text(message):
    for block in message.get("content", []):
        if "text" in block:
            return block["text"]
    return ""


REACT_SYSTEM_PROMPT = """You are a helpful assistant with access to tools.

Before taking any action, follow the ReAct pattern:
1. THINK: What does the user need? What information should I look up?
2. ACT: Choose the right tool and explain why.
3. OBSERVE: Analyze the tool result. Is it sufficient or do I need more?
4. RESPOND: Give a clear, complete answer based on all observations.

Wrap your reasoning in <thought>...</thought> tags so your thinking is visible.
Always explain your reasoning before calling a tool."""


def run_agent(user_message, system_prompt=REACT_SYSTEM_PROMPT, messages=None):
    """Run the agent loop with ReAct prompting and error handling."""
    if messages is None:
        messages = []
    messages.append({"role": "user", "content": [{"text": user_message}]})

    while True:
        response = client.converse(
            modelId=CLAUDE_SONNET,
            system=[{"text": system_prompt}],
            messages=messages,
            toolConfig={"tools": ALL_TOOLS},
        )
        assistant_msg = response["output"]["message"]
        messages.append(assistant_msg)

        if response["stopReason"] == "end_turn":
            return extract_text(assistant_msg), messages

        if response["stopReason"] == "tool_use":
            tool_results = []
            for block in assistant_msg["content"]:
                if "toolUse" in block:
                    name = block["toolUse"]["name"]
                    inp = block["toolUse"]["input"]
                    tid = block["toolUse"]["toolUseId"]
                    print(f"  [Tool] {name}({json.dumps(inp)})")

                    try:
                        result = TOOL_DISPATCH[name](**inp)
                    except Exception as e:
                        result = json.dumps({
                            "error": str(e),
                            "suggestion": "This tool is currently unavailable. Try answering without it or use a different approach."
                        })
                        print(f"  [Error] {result}")

                    tool_results.append({"toolResult": {"toolUseId": tid, "content": [{"text": str(result)}]}})
            messages.append({"role": "user", "content": tool_results})


def summarize_history(messages, keep_recent=4):
    """Summarize older messages to keep context manageable."""
    if len(messages) <= 10:
        return messages

    old_messages = messages[:-keep_recent]
    recent_messages = messages[-keep_recent:]

    conversation_text = ""
    for msg in old_messages:
        role = msg.get("role", "unknown")
        for block in msg.get("content", []):
            if "text" in block:
                conversation_text += f"{role}: {block['text'][:200]}\n"

    summary_response = client.converse(
        modelId=CLAUDE_HAIKU,
        system=[{"text": "Summarize this conversation concisely, preserving key facts and context."}],
        messages=[{"role": "user", "content": [{"text": conversation_text}]}],
    )
    summary = extract_text(summary_response["output"]["message"])

    return [{"role": "user", "content": [{"text": f"Previous conversation summary: {summary}"}]},
            {"role": "assistant", "content": [{"text": "Understood, I have the context from our previous conversation."}]}
            ] + recent_messages


def reflect_on_answer(question, answer):
    """Have the agent critique its own response and optionally revise."""
    reflection_prompt = f"""Review this Q&A pair. Is the answer accurate, complete, and well-structured?

Question: {question}
Answer: {answer}

Provide:
1. A brief critique (what's good, what could be better)
2. A revised answer if improvements are needed, or "No revision needed" if the answer is good."""

    response = client.converse(
        modelId=CLAUDE_SONNET,
        system=[{"text": "You are a quality reviewer. Be constructive but thorough."}],
        messages=[{"role": "user", "content": [{"text": reflection_prompt}]}],
    )
    return extract_text(response["output"]["message"])


if __name__ == "__main__":
    print("=== ReAct Agent ===")
    response, _ = run_agent("What's the weather in London and any recent banking news?")
    print(f"\nAgent: {response}\n")

    print("=== Error Handling Test ===")
    response, _ = run_agent("What's the stock price of NWG?")
    print(f"\nAgent: {response}\n")

    print("=== Reflection ===")
    question = "What is KYC?"
    answer, _ = run_agent(question)
    reflection = reflect_on_answer(question, answer)
    print(f"Reflection:\n{reflection}")
