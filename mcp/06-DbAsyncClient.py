import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client
import asyncio


async def run():
    async with httpx2.AsyncClient(
        headers={"Authorization": "Bearer ..."},
        timeout=httpx2.Timeout(30.0, read=300.0),
        follow_redirects=True,
    ) as http_client:
        transport = streamable_http_client(
            "http://localhost:8000/mcp",
            http_client=http_client,
        )
        async with Client(transport) as client:
            tools = await client.list_tools()
            print([tool.name for tool in tools.tools])

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