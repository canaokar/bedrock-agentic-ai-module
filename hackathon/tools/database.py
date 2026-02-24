"""
Hackathon Tool: SQLite Database
Simple SQLite query tool for agents.
"""

import json
import sqlite3

TOOL_SCHEMA = {
    "toolSpec": {
        "name": "query_database",
        "description": "Execute a read-only SQL query on the SQLite database.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL SELECT query to execute"},
                    "database": {"type": "string", "description": "Database file path (default: hackathon.db)"}
                },
                "required": ["query"]
            }
        }
    }
}

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "hackathon.db")


def _ensure_sample_db(db_path):
    """Create a sample database if it doesn't exist."""
    if os.path.exists(db_path):
        return
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            monthly_fee REAL,
            description TEXT
        )
    """)
    products = [
        (1, "Current Account", "accounts", 0, "Standard current account with debit card"),
        (2, "Savings Account", "accounts", 0, "Easy-access savings account"),
        (3, "Premium Account", "accounts", 15.00, "Premium account with travel insurance"),
        (4, "Personal Loan", "lending", 0, "Unsecured personal loan up to 25,000"),
        (5, "Mortgage", "lending", 0, "Residential mortgage products"),
        (6, "Credit Card", "cards", 0, "Standard credit card with cashback"),
        (7, "Business Account", "business", 8.50, "Business current account"),
    ]
    cur.executemany("INSERT OR IGNORE INTO products VALUES (?,?,?,?,?)", products)
    conn.commit()
    conn.close()


def query_database(query, database=None):
    """Execute a read-only SQL query."""
    db_path = database or DB_PATH
    _ensure_sample_db(db_path)

    if not query.strip().upper().startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries are allowed"})

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query)
        rows = [dict(row) for row in cur.fetchall()]
        conn.close()
        return json.dumps({"rows": rows, "count": len(rows)})
    except Exception as e:
        return json.dumps({"error": str(e)})
