from google.adk.agents import Agent
from google.adk.tools.google_search_tool import google_search

"""
A Userdefine (function) tool to get the current time.
"""
def get_current_time() -> dict:
    from datetime import datetime
    return {"current_time": datetime.now().isoformat()}

root_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description="Search agent",
    instruction="""
    you're a helpful assistance with help of tools below -
    get_current_time
    """,
    # tools=[google_search]
    tools=[get_current_time]
    # tools=[get_current_time,google_search] -> not possible to use build-in & userdefine tool together
)