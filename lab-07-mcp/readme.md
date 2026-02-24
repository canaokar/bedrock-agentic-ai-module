# Lab 07: MCP Server & Client

## Objective

Build an **MCP (Model Context Protocol) server** that exposes stock-market tools and resources, then build a **client** that discovers those tools and wires them into an Amazon Bedrock agent loop.

## What You Will Learn

- How to create an MCP server with `FastMCP`
- How to expose **tools** and **resources** via MCP
- How to connect to an MCP server from a Python client
- How to convert MCP tool schemas into Bedrock `toolConfig` format
- How to run a full agent loop: Bedrock calls MCP tools, results flow back

## Prerequisites

- Python 3.11+
- AWS credentials configured for Bedrock access
- `pip install -r requirements.txt`

## Files

| File | Description |
|------|-------------|
| `server.py` | MCP server exposing stock tools and resources |
| `client.py` | MCP client that discovers tools and runs a Bedrock agent loop |
| `requirements.txt` | Python dependencies |

## Tasks

### server.py (4 TODOs)

1. **TODO 1** - Implement `get_stock_price` tool
2. **TODO 2** - Implement `get_company_info` tool
3. **TODO 3** - Implement `market_summary` resource
4. **TODO 4** - Run the server (provided)

### client.py (5 TODOs)

1. **TODO 1** - Connect to the MCP server using `stdio_client`
2. **TODO 2** - List available tools from the server
3. **TODO 3** - Call a tool directly
4. **TODO 4** - Convert MCP tool schemas to Bedrock `toolConfig` format
5. **TODO 5** - Run a Bedrock agent loop that uses MCP tools

## Running

```bash
# The client launches the server automatically via stdio
python client.py
```

## Key Concepts

- **MCP Tools** are functions the server exposes for clients (or LLMs) to call
- **MCP Resources** are read-only data endpoints (like a REST GET)
- **stdio transport** connects client and server via stdin/stdout
- The client converts MCP schemas to Bedrock format so the LLM can decide which tools to call
