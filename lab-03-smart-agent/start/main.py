"""
Lab 03: Smart Agent
Enhance the basic agent with ReAct prompting, error handling, and conversation summarization.
"""

import boto3

import json
import time
from datetime import datetime

CLAUDE_SONNET = "us.anthropic.claude-sonnet-4-20250514"
CLAUDE_HAIKU = "us.anthropic.claude-haiku-4-20250514"
REGION = "ap-south-1"

client = boto3.client("bedrock-runtime", region_name=REGION)

# --- Tools (same as Lab 02, provided complete) ---
WEATHER_TOOL = {"toolSpec": {"name": "get_weather", "description": "Get current weather for a city.", "inputSchema": {"json": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}}
NEWS_TOOL = {"toolSpec": {"name": "search_news", "description": "Search recent news on a topic.", "inputSchema": {"json": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}}
TIME_TOOL = {"toolSpec": {"name": "get_time", "description": "Get current time in a timezone.", "inputSchema": {"json": {"type": "object", "properties": {"timezone": {"type": "string"}}, "required": ["timezone"]}}}}
# A deliberately broken tool for testing error handling
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


# TODO 1: Write a ReAct system prompt
# The prompt should instruct the model to:
# - THINK: What does the user need? What information should I look up?
# - ACT: Choose the right tool and explain why
# - OBSERVE: Analyze the tool result — is it sufficient?
# - RESPOND: Give a clear final answer based on observations
# Hint: Start with "Before taking any action, follow these steps..."
REACT_SYSTEM_PROMPT = ...


# TODO 2: Add structured output
# Modify the system prompt (or create a new one) that instructs the model to
# wrap its reasoning in <thought>...</thought> tags before each tool call.
# This makes the agent's reasoning visible and debuggable.
# Hint: Add to the system prompt: "Wrap your reasoning in <thought> tags."
STRUCTURED_SYSTEM_PROMPT = ...


def run_agent(user_message, system_prompt, messages=None):
    """Run the agent loop with ReAct prompting and error handling.

    Args:
        user_message: The user's message.
        system_prompt: The system prompt to use.
        messages: Optional conversation history.

    Returns:
        Tuple of (response_text, messages).
    """
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

                    # TODO 3: Add error handling around tool dispatch
                    # Wrap the tool call in try/except. On error, return a JSON
                    # string with the error message so the LLM can recover.
                    # Hint:
                    #   try:
                    #       result = TOOL_DISPATCH[name](**inp)
                    #   except Exception as e:
                    #       result = json.dumps({"error": str(e), "suggestion": "Try a different approach"})
                    result = TOOL_DISPATCH[name](**inp)  # Replace this line

                    tool_results.append({"toolResult": {"toolUseId": tid, "content": [{"text": str(result)}]}})
            messages.append({"role": "user", "content": tool_results})


def summarize_history(messages, keep_recent=4):
    """Summarize older messages to keep context manageable.

    When the conversation gets long (>10 messages), use the LLM to compress
    older messages into a single summary, keeping the most recent messages intact.

    Args:
        messages: The full message history.
        keep_recent: Number of recent messages to keep verbatim.

    Returns:
        A new, shorter messages list with older content summarized.
    """
    # TODO 4: Implement conversation summarization
    # 1. If len(messages) <= 10, return messages as-is
    # 2. Split into old_messages (everything except last keep_recent) and recent_messages
    # 3. Build a text summary of old_messages (just concatenate the text content)
    # 4. Call client.converse() with CLAUDE_HAIKU asking it to summarize the conversation
    # 5. Return: [{"role": "user", "content": [{"text": f"Previous conversation summary: {summary}"}]}] + recent_messages
    ...


def reflect_on_answer(question, answer):
    """Have the agent critique its own response and optionally revise.

    Args:
        question: The original user question.
        answer: The agent's answer to critique.

    Returns:
        The reflection text (critique + revised answer if needed).
    """
    # TODO 5 (BONUS): Implement reflection
    # Call CLAUDE_SONNET with a prompt like:
    # "Review this Q&A. Is the answer accurate, complete, and well-structured?
    #  If not, provide a revised answer."
    # Include both the question and answer in the prompt.
    ...


if __name__ == "__main__":
    # Test ReAct prompting
    if REACT_SYSTEM_PROMPT:
        print("=== ReAct Agent ===")
        response, _ = run_agent(
            "What's the weather in London and any recent banking news?",
            REACT_SYSTEM_PROMPT
        )
        print(f"\nAgent: {response}\n")

    # Test error handling (get_stock_price will fail)
    print("=== Error Handling Test ===")
    prompt = REACT_SYSTEM_PROMPT or "You are a helpful assistant."
    response, _ = run_agent("What's the stock price of NWG?", prompt)
    print(f"\nAgent: {response}\n")
