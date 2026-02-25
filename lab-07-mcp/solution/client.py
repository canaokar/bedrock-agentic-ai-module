"""
Lab 07 - MCP Client (Solution)
================================
Complete MCP client that connects to the server, discovers tools,
and wires them into an Amazon Bedrock agent loop.
"""

import asyncio
import os
from pathlib import Path
import json
import boto3

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

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
LLAMA = "meta.llama3-8b-instruct-v1:0"
MISTRAL = "mistral.ministral-3-3b-instruct"
REGION = "ap-south-1"
MODEL_ID = CLAUDE_HAIKU

bedrock = boto3.client("bedrock-runtime", region_name=REGION)


# ---------------------------------------------------------------------------
# TODO 4 - Convert MCP tool schemas to Bedrock toolConfig format
# ---------------------------------------------------------------------------
def mcp_to_bedrock_tools(mcp_tools) -> dict:
    """Convert MCP tool definitions to Bedrock converse() toolConfig format."""
    tools = []
    for tool in mcp_tools:
        # MCP inputSchema is a full JSON Schema dict; Bedrock wants it
        # nested under {"json": ...}.
        schema = tool.inputSchema
        # Remove keys Bedrock does not accept at the top level of inputSchema
        clean_schema = {
            "type": schema.get("type", "object"),
            "properties": schema.get("properties", {}),
        }
        if "required" in schema:
            clean_schema["required"] = schema["required"]

        tools.append(
            {
                "toolSpec": {
                    "name": tool.name,
                    "description": tool.description or tool.name,
                    "inputSchema": {"json": clean_schema},
                }
            }
        )
    return {"tools": tools}


# ---------------------------------------------------------------------------
# TODO 5 - Run a Bedrock agent loop with MCP tools
# ---------------------------------------------------------------------------
async def agent_loop(session, user_message: str):
    """Send a user message to Bedrock and let it call MCP tools as needed."""

    # 1. Discover MCP tools and convert to Bedrock format
    tools_result = await session.list_tools()
    tool_config = mcp_to_bedrock_tools(tools_result.tools)

    print(f"\nUser: {user_message}")
    print("-" * 40)

    # 2. Start the conversation
    messages = [{"role": "user", "content": [{"text": user_message}]}]

    while True:
        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=messages,
            toolConfig=tool_config,
        )

        stop_reason = response["stopReason"]
        output_message = response["output"]["message"]
        messages.append(output_message)

        # 3. If the model wants to use a tool, call it via MCP
        if stop_reason == "tool_use":
            tool_results = []
            for block in output_message["content"]:
                if "toolUse" in block:
                    tool_use = block["toolUse"]
                    tool_name = tool_use["name"]
                    tool_input = tool_use["input"]
                    tool_use_id = tool_use["toolUseId"]

                    print(f"  [Tool Call] {tool_name}({json.dumps(tool_input)})")

                    # Call the MCP tool
                    mcp_result = await session.call_tool(tool_name, tool_input)
                    result_text = (
                        mcp_result.content[0].text
                        if mcp_result.content
                        else "No result"
                    )
                    print(f"  [Tool Result] {result_text}")

                    tool_results.append(
                        {
                            "toolResult": {
                                "toolUseId": tool_use_id,
                                "content": [{"text": result_text}],
                            }
                        }
                    )

            # Feed tool results back to the model
            messages.append({"role": "user", "content": tool_results})

        # 4. If the model produced a final answer, print it and stop
        elif stop_reason == "end_turn":
            for block in output_message["content"]:
                if "text" in block:
                    print(f"\nAssistant: {block['text']}")
            break

        else:
            print(f"Unexpected stop reason: {stop_reason}")
            break


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main():
    print("MCP Client - Lab 07 (Solution)")
    print("=" * 40)

    # TODO 1 - Connect to the MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # TODO 2 - List available tools
            tools_result = await session.list_tools()
            print("\nDiscovered MCP Tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # TODO 3 - Call a tool directly
            print("\nDirect tool call - get_stock_price('NWG'):")
            result = await session.call_tool(
                "get_stock_price", {"symbol": "NWG"}
            )
            print(f"  {result.content[0].text}")

            # TODO 5 - Run the agent loop
            await agent_loop(
                session,
                "What is the stock price of NatWest and tell me about the company?",
            )


if __name__ == "__main__":
    asyncio.run(main())
