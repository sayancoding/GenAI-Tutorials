import streamlit as st

from app.doc_agent.agent import doc_agent
from app.utils import build_repo_context
from app.utils import clone_repo_to_local

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

import asyncio
import os
from dotenv import load_dotenv

#01 page configuration
st.set_page_config(
    page_title="AutoCodeDocsAI",
    page_icon="📝",
    layout="wide"
)
load_dotenv()

APP_NAME = "AutoCodeDocsAI"
SESSION_ID = "session_001"
USER_ID = "dev_user"

# 2. Asynchronous Logic Wrapper
async def run_agentic_workflow(repo_url):
    """Handles the cloning, context building, and ADK Runner execution."""
    
    # UI Step: Cloning & Context
    with st.status("🛠️ Preparation Phase", expanded=True) as status:
        st.write("Cloning repository...")
        local_repo_path = clone_repo_to_local(repo_url)
        
        st.write("Extracting code context...")
        context = build_repo_context(local_repo_path)
        status.update(label="Context Ready!", state="complete")

        # create a session for the agent to maintain state
        st.write("Creating session...")
        session_service = InMemorySessionService()
        session_service.create_session_sync(
            session_id=SESSION_ID,
            app_name=APP_NAME,
            user_id=USER_ID
        )

    # UI Step: Agent Reasoning
    st.info("🤖 Agent is analyzing the codebase...")
    
    # session_service = InMemorySessionService()
    runner = Runner(
        agent=doc_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    prompt = f"Please document this repository:\n{context}"
    user_message = types.Content(role="user", parts=[types.Part(text=prompt)])
    
    # We use a placeholder to stream the response live in Streamlit
    response_placeholder = st.empty()
    full_response = ""


    # Running ADK Async Loop
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message
    ):
        # In 2026, ADK supports partial streaming events
        if event.partial:
            for part in event.content.parts:
                full_response += part.text
                response_placeholder.markdown(full_response + "▌")
        
        if event.is_final_response():
            full_response = event.content.parts[0].text
            response_placeholder.markdown(full_response)
            return full_response

def main():
    st.title("🚀 Agentic Auto-Documenter")
    st.subheader("Turn any GitHub repo into professional documentation using Google ADK")

    with st.sidebar:
        st.header("Settings")
        st.warning("⚠️ This app uses Gemini 2.0 Flash, which may have associated costs. Please ensure you have the appropriate API key and understand the pricing before using.")
        api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
        st.caption("Powered by Gemini 2.0 Flash & Google ADK")

    repo_url = st.text_input("Enter GitHub Repository URL:", placeholder="https://github.com/user/repo")

    if st.button("Generate Documentation"):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar.")
            return
        if not repo_url:
            st.error("Please enter a valid GitHub repository URL.")
            return
        else:
            # Run the async workflow inside Streamlit
            readme_content = asyncio.run(run_agentic_workflow(repo_url))
            
            # Final Actions
            st.success("✅ Documentation Generated!")
            st.download_button(
                label="Download README.md",
                data=readme_content,
                file_name="README.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()