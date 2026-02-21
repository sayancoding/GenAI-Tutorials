from app.doc_agent.agent import doc_agent
from app.utils import build_repo_context
from app.utils import clone_repo_to_local

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

import asyncio
import os
from dotenv import load_dotenv



APP_NAME = "AutoDocApp"
SESSION_ID = "session_001"
USER_ID = "dev_user"

async def cloning_context_building(repo_url):

    # Cloning repo and building context
    print("Cloning repository and building context...")
    local_repo_path = clone_repo_to_local(repo_url)

    # GContext building from the cloned repo
    full_context = build_repo_context(local_repo_path)
    return full_context

async def start_auto_documentation(repo_path):
    #Step 1: Clone the repo and build context
    repo_url = input("Enter the Git repository URL to document: ")
    context = await cloning_context_building(repo_url)

    # create a session for the agent to maintain state
    session_service = InMemorySessionService()
    session_service.create_session_sync(
        session_id=SESSION_ID,
        app_name=APP_NAME,
        user_id=USER_ID
    )

    runner = Runner(
        agent=doc_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # Create the prompt for the agent
    prompt = f"Please document this repository:\n{context}"
    user_message = types.Content(
        role="user", 
        parts=[types.Part(text=prompt)]
    )
    
    # Trigger the Agent via the Runner
    print("Agent is analyzing the repository...")
    events = runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message
    )

    async for event in events:
        print("Received response from agent...")
        if event.is_final_response():
            readme_content = event.content.parts[0].text
            return readme_content

if __name__ == "__main__":
    load_dotenv()
    repo_path = "."
    readme_content = asyncio.run(start_auto_documentation(repo_path))
    print("Generated README.md Content:\n")
    print(readme_content)