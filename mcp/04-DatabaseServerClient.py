from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

# StdioServerParameters is configuration only — always wrap with stdio_client(...)
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["03-DatabaseServer.py"],  # Server script
    env=None,  # Pass API keys here if needed; the child does not inherit your full env
)


async def run():
    # Client takes the transport; async with opens the connection
    async with Client(stdio_client(server_params)) as client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:", [tool.name for tool in tools.tools])

        db_path = "c:\\database\\fintech.db"

        # call_tool returns CallToolResult — prefer structured_content for application code
        tables = await client.call_tool("list_tables", {"db_path": db_path})
        print("Tables in database:", tables.structured_content)

        schema = await client.call_tool("get_table_schema", {
            "db_path": db_path,
            "table_name": "users"
        })
        print("Table schema for users:", schema.structured_content)

        results = await client.call_tool("execute_query", {
            "db_path": db_path,
            "query": "SELECT * FROM users LIMIT 5"
        })
        print("First 5 users:", results.structured_content)

if __name__ == "__main__":
    asyncio.run(run())