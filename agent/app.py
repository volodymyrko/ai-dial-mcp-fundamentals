import asyncio
import json
import os

from mcp import Resource
from mcp.types import Prompt

from agent.mcp_client import MCPClient
from agent.dial_client import DialClient
from agent.models.message import Message, Role
from agent.prompts import SYSTEM_PROMPT

DIAL_ENDPOINT = "https://ai-proxy.lab.epam.com"
API_KEY = os.getenv('DIAL_API_KEY')

# https://remote.mcpservers.org/fetch/mcp
# Pay attention that `fetch` doesn't have resources and prompts

async def main():
    #TODO:
    # 1. Create MCP client and open connection to the MCP server (use `async with {YOUR_MCP_CLIENT} as mcp_client`),
    #    mcp_server_url="http://localhost:8005/mcp"
    # 2. Get Available MCP Resources and print them
    # 3. Get Available MCP Tools, assign to `tools` variable, print tool as well
    # 4. Create DialClient
    # 5. Create list with messages and add there SYSTEM_PROMPT with instructions to LLM
    # 6. Add to messages Prompts from MCP server as User messages
    # 7. Create console chat (infinite loop + ability to exit from chat + preserve message history after the call to dial client)
    # raise NotImplementedError()
    async with MCPClient('http://localhost:8005/mcp') as mcp_client:
        resources = await mcp_client.get_resources()
        print(f'mcp resources: {resources}\n')

        tools = await mcp_client.get_tools()
        print(f'mcp tools: {tools}\n')

        dial_client = DialClient(api_key=API_KEY, endpoint=DIAL_ENDPOINT, tools=tools, mcp_client=mcp_client)

        messages = [Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)]

        prompt_results = await mcp_client.get_prompts()
        if prompt_results:
            for prompt in prompt_results.prompts:
                content = await mcp_client.get_prompt(prompt.name)
                messages.append(
                    Message(
                        role=Role.USER,
                        content=f'## Prompt provided by MCP server: {prompt.description}\n{content}')
                )

        print('Ask the question')
        while True:
            user_question = input('> ').strip()

            if user_question == 'exit':
                print('Exiting')
                break

            messages.append(Message(role=Role.USER, content=user_question))
            ai_response = await dial_client.get_completion(messages)

            print('api response:', ai_response)

            messages.append(ai_response)



if __name__ == "__main__":
    asyncio.run(main())
