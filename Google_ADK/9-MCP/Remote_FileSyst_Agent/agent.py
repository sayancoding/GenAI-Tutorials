from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams

from mcp import StdioServerParameters

import os

from .model import gemini_llm

LLM = gemini_llm
TARGET_FOLDER = os.path.join(os.path.dirname(__file__),"resource","..")

root_agent = Agent(
    name="FileSystem_Agent",
    description="You're a file system specialist assistant",
    model= LLM,
    instruction="Help user to mange thier file, like list-files, read-file etc", 
    tools=[
        MCPToolset(
            connection_params = StdioConnectionParams(
                server_params= StdioServerParameters(
                    # As getting TimeOut error from execution
                    # firstly --> npm install -g @modelcontextprotocol/server-filesystem
                    # secondly --> use the pakage to start the server
                    
                    command="mcp-server-filesystem",
                    args=[
                        os.path.abspath(TARGET_FOLDER)
                    ]
                )
            ),
            tool_filter = ['list_directory', 'read_file']
        )
    ]
)
