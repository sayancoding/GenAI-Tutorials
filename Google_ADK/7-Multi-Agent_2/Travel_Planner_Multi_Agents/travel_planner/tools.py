from google.adk.tools.google_search_tool import google_search
from google.adk.agents import Agent
from .models import gemini_llm,open_router_llm

llm = gemini_llm

_search_agent_tool = Agent(
    model=llm,
    name="Travel_Search_Tool_Agent",
    description="Agent that uses Google Search to find latest & relevant travel information.",
    instruction="""
        - You have access to the Google Search Tool.
        - Use it to find up-to-date information about travel destinations, attractions, and more.
        - Provide concise and relevant information based on user preferences.
        - Always show 2-3 search result with bullet points.
    """,
    tools=[google_search],
)