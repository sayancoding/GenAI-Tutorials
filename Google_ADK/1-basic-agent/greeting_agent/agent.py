from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

local_model = LiteLlm(
    model="ollama_chat/gemma3:1b", 
    api_base="http://localhost:11434")

root_agent = Agent(
    name="greeting_agent",
    model=local_model,
    description="Greeting agent",
    instruction="""
    you're a helpful assistance that greets the user.
    Ask for user's name and greet them by name and reply in concise way
    """
)