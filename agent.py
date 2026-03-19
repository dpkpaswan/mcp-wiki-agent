import sys
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

async def create_agent():
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command=sys.executable,
            args=["mcp_server.py"],
        )
    )
    agent = Agent(
        name="wiki_info_agent",
        model="groq/llama-3.1-8b-instant",
        description="Research assistant using Wikipedia via MCP.",
        instruction="""You are a helpful research assistant.
Use the search_wikipedia tool to fetch accurate information.
Always summarize clearly and mention data came from Wikipedia.""",
        tools=tools,
    )
    return agent, exit_stack