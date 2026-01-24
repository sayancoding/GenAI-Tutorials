import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

"""
A Userdefine (function) tool to get the current time.
"""
def get_current_time() -> dict:
    from datetime import datetime
    return {"current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

model = LiteLlm(
    model='openrouter/x-ai/grok-4.1-fast:free',
    api_key = os.getenv("OPENROUTER_API_KEY")
)

root_agent = Agent(
    name="search_agent",
    model=model,
    description="Search agent",
    instruction="""
    you're a helpful assistance with help of tools below -
    get_current_time
    """,
    # tools=[google_search]
    tools=[get_current_time]
    # tools=[get_current_time,google_search] -> not possible to use build-in & userdefine tool together
)