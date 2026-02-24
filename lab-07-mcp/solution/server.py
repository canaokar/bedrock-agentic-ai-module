"""
Lab 07 - MCP Server (Solution)
================================
A complete MCP server exposing stock-market tools and resources.
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
@mcp.tool()
def get_stock_price(symbol: str) -> str:
    """Get the current stock price for a given ticker symbol."""
    symbol = symbol.upper()
    if symbol not in STOCK_PRICES:
        return f"Error: Unknown symbol '{symbol}'. Available: {', '.join(STOCK_PRICES)}"
    data = STOCK_PRICES[symbol]
    direction = "+" if data["change"] >= 0 else ""
    return (
        f"{symbol}: {data['currency']} {data['price']:.2f} "
        f"({direction}{data['change']:.2f})"
    )


# ---------------------------------------------------------------------------
# TODO 2 - get_company_info tool
# ---------------------------------------------------------------------------
@mcp.tool()
def get_company_info(name: str) -> str:
    """Get company information by company name."""
    # Try case-insensitive match
    match = None
    for key, info in COMPANY_INFO.items():
        if key.lower() == name.lower():
            match = info
            break

    if match is None:
        return f"Error: Unknown company '{name}'. Available: {', '.join(COMPANY_INFO)}"

    return (
        f"Company: {name}\n"
        f"  Symbol: {match['symbol']}\n"
        f"  Sector: {match['sector']}\n"
        f"  Employees: {match['employees']:,}\n"
        f"  Headquarters: {match['headquarters']}"
    )


# ---------------------------------------------------------------------------
# TODO 3 - market summary resource
# ---------------------------------------------------------------------------
@mcp.resource("market://summary")
def market_summary() -> str:
    """Get a summary of all tracked stocks."""
    lines = ["Market Summary", "=" * 40]
    for symbol, data in STOCK_PRICES.items():
        direction = "+" if data["change"] >= 0 else ""
        lines.append(
            f"  {symbol}: {data['currency']} {data['price']:.2f} "
            f"({direction}{data['change']:.2f})"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# TODO 4 - Run the server
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
