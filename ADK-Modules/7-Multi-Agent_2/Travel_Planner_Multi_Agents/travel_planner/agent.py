from google.adk.agents import Agent

from .sub_agents import travel_inspiration_agent
from .models import gemini_llm,open_router_llm

llm = gemini_llm

root_agent = Agent(
    model=llm,
    name="Travel_Planner_Root_Agent",
    description="helpful travel planning assistant that helps users plan their trips by providing information and give suggestion based on their preference",
    instruction="""
        - You are the lead travel concierge.
        - Your ONLY job is to greet the user and delegate the research to the 'Travel_Inspiration_Agent'.
        - ONCE the Travel_Inspiration_Agent provides the travel points, do NOT delegate again. 
        - Simply present the information to the user as the final answer.
    """,
    sub_agents=[travel_inspiration_agent]
)