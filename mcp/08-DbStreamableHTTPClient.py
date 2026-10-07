from mcp import Client
import asyncio


async def run():
    # A URL string uses Streamable HTTP
    async with Client("http://localhost:8000/mcp") as client:
        tools = await client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools.tools]}")

        db_path = "c:\\database\\fintech.db"

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