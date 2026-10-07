from mcp import StdioServerParameters, Client
from mcp.client.stdio import stdio_client


async def run():

    server_params= StdioServerParameters(
        command="python",
        args=["C:\\npci-mumbai\\ws\\mcpdemo\\MyDbMcpServer.py"]
    )

    async with Client(stdio_client(server_params)) as client:
        tools = await client.list_tools()

        #print(tools.tools)

        for tool in tools.tools:
            print(f"{tool.name}  -- desc -{tool.description}")

        response = await  client.call_tool("list_tables", {"db_path": "C:\\npci-mumbai\\ws\\fintech.db"})

        #print(response.content)

        for content in response.content:
            print(content.text)


if __name__== "__main__":

    import asyncio
    asyncio.run(run())





