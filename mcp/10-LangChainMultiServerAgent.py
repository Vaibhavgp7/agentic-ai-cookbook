from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
import asyncio

# Ensure you have OPENAI_API_KEY set in your environment
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"
from dotenv import load_dotenv
load_dotenv()
config = {
    "mcpServers": {
        "filesystem": {
            "command": "python",
            "args": [r"C:\Users\Training\Downloads\AgenticTraining\mcp\01-FileSystemServer.py"],
        },
        "database": {
            # Make sure DatabaseServerStreamableHTTP is running on port 8000
            "url": "http://localhost:8000/mcp",
        },
    }
}


async def main():
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")

        agent = create_agent("openai:gpt-4o-mini", tools)

        print("\n" + "=" * 80)
        print("Multi-Server Task: Query database and save results to file")
        print("=" * 80)
        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": """First, get the first 5 users from the users table in c:\\database\\fintech.db.
        Then, write these results to a file named c:\\database\\top5_users.txt.
        Finally, read and show me the contents of the file."""}]
        })
        print(f"\nResult: {result['messages'][-1].content}\n")

        print("\n" + "=" * 80)
        print("File System Task: List files in database directory")
        print("=" * 80)
        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": "List all files in the c:\\database directory"}]
        })
        print(f"\nResult: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    asyncio.run(main())