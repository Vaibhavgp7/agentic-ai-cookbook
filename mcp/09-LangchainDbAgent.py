from pathlib import Path
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
import asyncio

# Ensure you have OPENAI_API_KEY set in your environment
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

from dotenv import load_dotenv
load_dotenv()
async def main():
    # Path = local script over stdio (must be Path, not a string)
    async with MCPAdapter(Path("03-DatabaseServer.py")) as adapter:
        tools = await adapter.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")

        agent = create_agent("openai:gpt-4o-mini", tools)

        print("\n" + "=" * 80)
        print("List all tables in the fintech database")
        print("=" * 80)
        result = await agent.ainvoke({
            "messages": [{
                "role": "user",
                "content": "List all tables in the database located at c:\\database\\fintech.db",
            }]
        })
        print(f"\nResult: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    asyncio.run(main())