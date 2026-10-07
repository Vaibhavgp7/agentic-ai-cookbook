from mcp.server import MCPServer
import sqlite3
from typing import List, Dict, Any
from pathlib import Path

# Name the server here
mcp = MCPServer("DatabaseServerStreamable")

# Other run() options (examples):
# mcp.run(transport="streamable-http", stateless_http=True)  # streaming responses
# mcp.run(transport="streamable-http")  # Stateful with session persistence

@mcp.tool()
def list_tables(db_path: str) -> List[str]:
    """List all tables in the database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        return [f"Error listing tables: {str(e)}"]

@mcp.tool()
def get_table_schema(db_path: str, table_name: str) -> str:
    """Get schema information for a specific table as a CREATE TABLE string"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name=?;",
            (table_name,),
        )
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            return row[0]
        return f"Table '{table_name}' not found"
    except Exception as e:
        return f"Error getting schema: {str(e)}"

@mcp.tool()
def execute_query(db_path: str, query: str) -> List[Dict[str, Any]]:
    """Execute a SQL query and return results"""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    except Exception as e:
        return [{"error": f"Error executing query: {str(e)}"}]

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        port=8000,
        stateless_http=True,
        json_response=True,
    )