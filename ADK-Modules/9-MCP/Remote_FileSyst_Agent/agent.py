from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams

from mcp import StdioServerParameters

import os

from .model import local_llm

LLM = local_llm
TARGET_FOLDER = os.path.join(os.path.dirname(__file__))

root_agent = Agent(
    name="FileSystem_Agent",
    description="You're a file system specialist assistant",
    model= LLM,
    instruction="Help user to mange thier file, like list-files, read-file etc", 
    tools=[
        MCPToolset(
            connection_params = StdioConnectionParams(
                server_params= StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        os.path.abspath(TARGET_FOLDER).replace("/", "\\")
                    ]
                )
            ),
            tool_filter = ['list_directory', 'read_file']
        )
    ]
)
