"""
Lab 07 - MCP Client (Start)
============================
Build an MCP client that connects to the server, discovers its tools,
and wires them into an Amazon Bedrock agent loop.

Your tasks:
  TODO 1 - Connect to the MCP server
  TODO 2 - List available tools
  TODO 3 - Call a tool directly
  TODO 4 - Convert MCP tool schemas to Bedrock toolConfig format
  TODO 5 - Run a Bedrock agent loop that uses MCP tools
"""

import asyncio
import json
import boto3

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CLAUDE_SONNET = "us.anthropic.claude-sonnet-4-20250514"
CLAUDE_HAIKU = "us.anthropic.claude-haiku-4-20250514"
REGION = "ap-south-1"
MODEL_ID = CLAUDE_HAIKU

bedrock = boto3.client("bedrock-runtime", region_name=REGION)


# ---------------------------------------------------------------------------
# TODO 1 - Connect to the MCP server
# ---------------------------------------------------------------------------
# Create StdioServerParameters that launches "python server.py" and use
# stdio_client + ClientSession to connect.
#
# Hint:
#   server_params = StdioServerParameters(
#       command="python",
#       args=["server.py"],
#   )
#   async with stdio_client(server_params) as (read_stream, write_stream):
#       async with ClientSession(read_stream, write_stream) as session:
#           await session.initialize()
#           ...


# ---------------------------------------------------------------------------
# TODO 2 - List available tools
# ---------------------------------------------------------------------------
# Use session.list_tools() to discover what tools the server exposes.
# Print each tool's name, description, and input schema.
#
# Hint:
#   tools_result = await session.list_tools()
#   for tool in tools_result.tools:
#       print(tool.name, tool.description, tool.inputSchema)


# ---------------------------------------------------------------------------
# TODO 3 - Call a tool directly
# ---------------------------------------------------------------------------
# Use session.call_tool(name, arguments) to invoke get_stock_price for "NWG".
# Print the result.
#
# Hint:
#   result = await session.call_tool("get_stock_price", {"symbol": "NWG"})
#   print(result)


# ---------------------------------------------------------------------------
# TODO 4 - Convert MCP tool schemas to Bedrock toolConfig format
# ---------------------------------------------------------------------------
# Bedrock expects tools in this shape:
#   {
#       "tools": [
#           {
#               "toolSpec": {
#                   "name": "...",
#                   "description": "...",
#                   "inputSchema": { "json": { ... JSON Schema ... } }
#               }
#           }
#       ]
#   }
#
# Write a function that takes the MCP tools list and returns this structure.
#
# def mcp_to_bedrock_tools(mcp_tools) -> dict:
#     ...


# ---------------------------------------------------------------------------
# TODO 5 - Run a Bedrock agent loop with MCP tools
# ---------------------------------------------------------------------------
# 1. Convert MCP tools to Bedrock format (TODO 4).
# 2. Send a user message + toolConfig to Bedrock converse().
# 3. When Bedrock returns a toolUse block, call the MCP tool via
#    session.call_tool() and return the result back to Bedrock.
# 4. Loop until Bedrock produces a final text response.
#
# async def agent_loop(session, user_message: str):
#     ...


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main():
    print("MCP Client - Lab 07")
    print("=" * 40)
    # Wire together TODOs 1-5 here.
    # 1. Connect to server
    # 2. List tools
    # 3. Call a tool directly
    # 4. Run the agent loop with a question like
    #    "What is the stock price of NatWest and tell me about the company?"
    pass


if __name__ == "__main__":
    asyncio.run(main())
