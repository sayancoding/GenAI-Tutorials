import streamlit as st
import asyncio
import os
import time
from dotenv import load_dotenv

from app.doc_agent.agent import doc_agent  # Agent already has MCP wired in
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from mcp.shared.exceptions import McpError

st.set_page_config(
    page_title="AutoCodeDocsAI - With MCP",
    page_icon="🤖",
    layout="wide"
)
load_dotenv()

APP_NAME = "AutoCodeDocsAI"
SESSION_ID = "session_001"
USER_ID = "dev_user"


async def run_agentic_workflow(repo_url):
    # ✅ No manual MCP setup — it's handled inside the agent definition
    session_service = InMemorySessionService()
    session_service.create_session_sync(
        session_id=SESSION_ID,
        app_name=APP_NAME,
        user_id=USER_ID
    )

    st.info(f"🤖 Agent is analyzing repository: {repo_url}")

    runner = Runner(
        agent=doc_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # Create a unique branch name based on the current timestamp
    # This ensures "feature/auto-docs-1713354000" is always unique
    timestamp = int(time.time())
    unique_branch = f"feature/auto-docs-{timestamp}"

    prompt = (
        f"""Target Repository: {repo_url} 
         Owner/Repo: {repo_url} 
         Action: Analyis Repo & Create a professional README and submit a PR.
         Use the branch name: '{unique_branch}' for this task.
        
        STRICT PROTOCOL:
        1. Do not just describe your plan. 
        2. You MUST execute the tools 'create_branch', 'create_or_update_file', and 'create_pull_request' in sequence.
        3. Your task is only 'Complete' once you provide the URL of the submitted Pull Request.
        4. If you have the README content and SHA, proceed immediately to 'create_branch'.
        """
    )

    user_message = types.Content(role="user", parts=[types.Part(text=prompt)])

    # Create a dedicated area for the agent's thought process
    thinking_container = st.container()
    response_placeholder = st.empty()
    full_response = ""

    with st.status("🤖 Agent at work...", expanded=True) as status:
        try: 
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=user_message
            ):
                # 1. Handle Working Phase (Tool Calls)
                if event.get_function_calls():
                    for call in event.get_function_calls():
                        with thinking_container:
                            with st.expander(f"Action: {call.name}", expanded=False):
                                st.json(call.args)

                # 2. Handle Thinking Phase (Text)
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            full_response += part.text
                            response_placeholder.markdown(full_response + "▌")

                # 3. Check for completion
                if event.is_final_response():
                    status.update(label="✅ Agent task is Completed!", state="complete")
                    if "SPull Request created" not in full_response.lower():
                        st.warning("⚠️ The agent finished but didn't provide a PR link. It might have stopped early.")
                    return full_response
                pass
        except McpError as e:
            if "Reference already exists" in str(e):
                st.warning("⚠️ Branch already exists! Please delete it on GitHub or change the branch name.")
                return "Error: Branch Collision"
            else:
                st.error(f"GitHub MCP Error: {e}")
                return None    
    
    # Final output
    display_text = full_response.replace("\n", "\n\n") 
    response_placeholder.markdown(display_text)
    return full_response

def main():
    st.title("🚀 Agentic Auto-Documenter (MCP)")
    st.subheader("Autonomous Documentation via Model Context Protocol")

    with st.sidebar:
        st.header("System Status")
        if os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
            st.success("GitHub Token: Loaded")
        else:
            st.error("GitHub Token: Missing")
        st.caption("Using Gemini 2.0 Flash + GitHub MCP Server")

    repo_url = st.text_input(
        "Enter GitHub Repository URL:",
        placeholder="e.g., https://github.com/sayancoding/MyProject"
    )

    if st.button("Generate & PR Documentation"):
        if not repo_url:
            st.error("Please enter a valid GitHub repository URL.")
        else:
            readme_content = asyncio.run(run_agentic_workflow(repo_url))
            st.success("✅ Workflow Complete!")
            if readme_content:
                st.markdown("### Agent Summary")
                st.download_button("Download Draft README", readme_content, "README.md")


if __name__ == "__main__":
    main()