"""
Lab 07 - MCP Server (Start)
============================
Build an MCP (Model Context Protocol) server using FastMCP.

This server exposes tools and resources that an MCP client (or an LLM agent)
can discover and invoke at runtime.

Your tasks:
  TODO 1 - Implement the get_stock_price tool
  TODO 2 - Implement the get_company_info tool
  TODO 3 - Implement the market summary resource
  TODO 4 - Run the server (already provided)
"""

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Create the MCP server instance
# ---------------------------------------------------------------------------
mcp = FastMCP("StockMarket")

# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------
STOCK_PRICES = {
    "NWG": {"price": 4.12, "currency": "GBP", "change": +0.08},
    "AAPL": {"price": 227.50, "currency": "USD", "change": -1.25},
    "GOOGL": {"price": 178.30, "currency": "USD", "change": +2.10},
}

COMPANY_INFO = {
    "NatWest": {
        "symbol": "NWG",
        "sector": "Financial Services",
        "employees": 61_000,
        "headquarters": "Edinburgh, UK",
    },
    "Apple": {
        "symbol": "AAPL",
        "sector": "Technology",
        "employees": 164_000,
        "headquarters": "Cupertino, CA",
    },
    "Google": {
        "symbol": "GOOGL",
        "sector": "Technology",
        "employees": 182_000,
        "headquarters": "Mountain View, CA",
    },
}

# ---------------------------------------------------------------------------
# TODO 1 - get_stock_price tool
# ---------------------------------------------------------------------------
# Create a tool decorated with @mcp.tool() that:
#   - Takes a stock symbol (str) as input
#   - Looks it up in STOCK_PRICES
#   - Returns a formatted string with price, currency, and change
#   - Returns an error message if the symbol is not found
#
# Hint:
#   @mcp.tool()
#   def get_stock_price(symbol: str) -> str:
#       ...


# ---------------------------------------------------------------------------
# TODO 2 - get_company_info tool
# ---------------------------------------------------------------------------
# Create a tool decorated with @mcp.tool() that:
#   - Takes a company name (str) as input
#   - Looks it up in COMPANY_INFO
#   - Returns a formatted string with symbol, sector, employees, HQ
#   - Returns an error message if the company is not found
#
# Hint:
#   @mcp.tool()
#   def get_company_info(name: str) -> str:
#       ...


# ---------------------------------------------------------------------------
# TODO 3 - market summary resource
# ---------------------------------------------------------------------------
# Create a resource decorated with @mcp.resource("market://summary") that:
#   - Returns a string summarising all stocks in STOCK_PRICES
#   - Include symbol, price, and change for each stock
#
# Hint:
#   @mcp.resource("market://summary")
#   def market_summary() -> str:
#       ...


# ---------------------------------------------------------------------------
# TODO 4 - Run the server (provided)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
