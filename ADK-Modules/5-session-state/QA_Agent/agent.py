from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv;

load_dotenv()

model = LiteLlm(
    model='openrouter/nex-agi/deepseek-v3.1-nex-n1:free',
    api_key = os.getenv("OPENROUTER_API_KEY")
)


root_agent = Agent(
    name="QA_Agent",
    description="Question and Ansering Agent",
    # model="gemini-2.0-flash",
    model=model,
    instruction="""
    You are a helpful assistant that answers questions based on the provided context.
    here some info about user:
    username: {user_name}
    user-preferences: {user_preferences}  
    """
)