from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .models import gemini_llm,open_router_llm
from .tools import _search_agent_tool

llm = gemini_llm

travel_inspiration_agent = Agent(
    model=llm,
    name="Travel_Inspiration_Agent",
    description="Inspires users with travel ideas.",
    instruction="""
        - You are the research specialist.
        - Based on user preferences, provide 3-5 concise bullet points for destinations.
        - Once you provide these points, signal that your task is complete.
        - For latest news research purpose only use the 'Travel_Search_Tool_Agent' tool and format the response from the tool appropriately.
    """,
    tools=[AgentTool(agent=_search_agent_tool)]
)