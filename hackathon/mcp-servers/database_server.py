"""
Hackathon MCP Server: Database
Exposes a SQLite database as MCP tools for agent consumption.
"""

from mcp.server.fastmcp import FastMCP
import sqlite3
import json

mcp = FastMCP("database-server")

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "hackathon.db")


def _ensure_db():
    """Create sample database if it doesn't exist."""
    if os.path.exists(DB_PATH):
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY, name TEXT, category TEXT,
            monthly_fee REAL, description TEXT
        )
    """)
    products = [
        (1, "Current Account", "accounts", 0, "Standard current account with debit card"),
        (2, "Savings Account", "accounts", 0, "Easy-access savings account"),
        (3, "Premium Account", "accounts", 15.00, "Premium account with travel insurance"),
        (4, "Personal Loan", "lending", 0, "Unsecured personal loan up to 25,000"),
        (5, "Credit Card", "cards", 0, "Standard credit card with cashback"),
    ]
    cur.executemany("INSERT OR IGNORE INTO products VALUES (?,?,?,?,?)", products)
    conn.commit()
    conn.close()


@mcp.tool()
def query_database(sql: str) -> str:
    """Execute a read-only SQL query on the database.

    Args:
        sql: A SQL SELECT statement to execute.
    """
    _ensure_db()
    if not sql.strip().upper().startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries are allowed"})
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = [dict(r) for r in conn.execute(sql).fetchall()]
        conn.close()
        return json.dumps({"rows": rows, "count": len(rows)})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def list_tables() -> str:
    """List all tables in the database."""
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    conn.close()
    return json.dumps({"tables": tables})


@mcp.tool()
def describe_table(table_name: str) -> str:
    """Get the schema of a database table.

    Args:
        table_name: Name of the table to describe.
    """
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    columns = [{"name": r[1], "type": r[2]} for r in
               conn.execute(f"PRAGMA table_info({table_name})").fetchall()]
    conn.close()
    return json.dumps({"table": table_name, "columns": columns})


if __name__ == "__main__":
    mcp.run(transport="stdio")
