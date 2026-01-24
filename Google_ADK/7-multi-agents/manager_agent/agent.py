from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .tools.tools import get_current_time
from .sub_agents.news_agent.agent import news_analyst
from .sub_agents.stock_agent.agent import stock_analyst
from google.adk.models.lite_llm import LiteLlm
import os

lite_model = LiteLlm(
    model="ollama_chat/gemma3:4b", 
    api_base="http://localhost:11434"
)

root_agent = Agent(
    name="manager_agent",
    description="An agent that manages multiple sub-agents and tools to perform complex tasks.",
    model=lite_model,
    instruction="""
    You're the manager. Always delegate the task to the appropriate agent and tools to perform complex tasks.
    sub agents are below - 
    1. stock_analyst
    2. news_analyst
    tools are below - 
    1. get_current_time
    """,
    sub_agents=[stock_analyst],
    tools=[get_current_time, AgentTool(agent=news_analyst)]
)