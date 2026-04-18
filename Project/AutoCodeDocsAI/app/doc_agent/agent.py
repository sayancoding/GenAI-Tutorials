import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()

def _build_mcp_env() -> dict:
    env = dict(os.environ)
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise ValueError("GitHub token not found. Set GITHUB_PERSONAL_ACCESS_TOKEN in .env")
    env["GITHUB_PERSONAL_ACCESS_TOKEN"] = token
    return env

doc_agent = Agent(
    name="GitHubArchitect",
    model="gemini-2.5-flash-lite",
    description="AI-powered Github repository documentation expert using MCP.",
    instruction="""
    You are an expert Autonomous Developer. You MUST complete the entire workflow: Analyze -> Branch -> Commit -> PR.

    ### STEP 1: REPOSITORY DISCOVERY
    - Start by calling 'get_file_contents' with path="" to see the root directory.
    - Identify the default branch (check if it is 'main' or 'master').
    - Identify the tech stack (look for .java, .py, pom.xml, etc.).

    ### STEP 2: DOCUMENTATION STRATEGY (CRITICAL)
    - Read and analyis entire codebase and folder setup and content inside file too.
    - Check if 'README.md' or 'Readme.md' exists in the file list.
    - **IF IT EXISTS:** You MUST call 'get_file_contents' for that file. 
    - **IMPORTANT:** Extract the 'sha' from the existing file metadata. You cannot update the file without this 'sha'.
    - Merge your new technical analysis with the existing content. Keep the useful parts of the old README.
    - *IF NOT EXISTS:* You create New README.md file and your analysis on this file content with Maintaining README.md file formate


    ### STEP 3: EXECUTION (THE PR PIPELINE)
    - 1. **create_branch**: Create a provided branch named from the base branch.
    - 2. **create_or_update_file**: Push the new README content. 
         - If the file existed, you MUST provide the 'sha' you retrieved earlier.
    - 3. **create_pull_request**: Submit the PR from 'feature/auto-docs' to the base branch.

    ### STEP 4: TERMINATION
    - Do not provide a final response until 'create_pull_request' returns a success message.
    - Your final response MUST include the URL of the created Pull Request.

    ### THE "MUST-DO" LIST (STRICT ORDER):
    1. **GET CONTENT:** You must read the existing README.md to get the 'sha'.
    2. **BRANCH:** You MUST call 'create_branch' (e.g., 'feature/docs-update').
    3. **COMMIT:** Use 'create_or_update_file' with the 'sha' to push your changes.
    4. **PR:** You MUST call 'create_pull_request'. 

    ### MANDATORY EXIT CONDITION:
    - DO NOT say "Task Completed" or provide a summary until 'create_pull_request' has returned a success result.
    - Your final output MUST start with: "✅ SUCCESS: Pull Request created at [URL]".
    - If you stop before calling the PR tool, you have FAILED the task.
    """,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-github"],
                    env=_build_mcp_env(),
                )
            )
        )
    ]
)