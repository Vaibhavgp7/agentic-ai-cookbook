from langchain.mcp import MCPAdapter
from pathlib import Path
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()


async def run():

   config = {
        "mcpServers": {
            "gmail": {
                "command": "npx",
                "args": ["-y", "@gongrzhe/server-gmail-autoauth-mcp"],
            },
        }
    }



   async with  MCPAdapter(config) as adapter:
      tools = await adapter.list_tools()

      agent = create_agent(
         model= ChatOpenAI(model="gpt-4.1-mini"),
         tools=tools
      )

      result= await  agent.ainvoke(
         {
            "messages": [
               HumanMessage(content="send a mail to sivaprasad.valluru@gmail.com reminding him anout training tomorrow at 9 AM")
            ]

         }
      )

      print("Mail Sent")
      print(result['messages'])
    #   for tool in tools:
    #      print(tool.name)


if __name__== "__main__":
   import asyncio

   asyncio.run(run())