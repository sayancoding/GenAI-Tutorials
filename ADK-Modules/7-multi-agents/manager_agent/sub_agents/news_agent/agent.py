from google.adk.agents import Agent
from google.adk.tools.google_search_tool import google_search
from google.adk.models.lite_llm import LiteLlm
import os

lite_model = LiteLlm(
    model="ollama_chat/gemma3:4b", 
    api_base="http://localhost:11434"
)

news_analyst = Agent(
    name="news_agent",
    description="An agent that provides the latest news updates.",
    model=lite_model,
    instruction="""
    You're a news agent. Provide the latest 5 news updates summary with headline based on user queries in very concise way.""",
    tools=[google_search]
)