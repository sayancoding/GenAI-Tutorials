import uuid
import asyncio
import os
import warnings
from dotenv import load_dotenv;
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from QA_Agent.agent import root_agent as qa_agent

# Suppress litellm async cleanup warning
warnings.filterwarnings("ignore", message=".*close_litellm_async_clients.*")

load_dotenv()


async def main():
    # Create an in-memory session service
    session_service = InMemorySessionService()

    initial_state = {
        "user_name": "Sayan",
        "user_preferences": """
            Interested in technology and programming.
            Hobby is playing guitar
            Favourite food is Chicken & Biryani
            25 years old and Indian 
            working at IT Industry
        """
    }

    # Create a new session with a unique ID and initial state
    SESSION_ID = str(uuid.uuid4())
    APP_NAME = "Sayan Bot"
    USER_ID = "sayan_123"

    stateful_session = await session_service.create_session(
        session_id=SESSION_ID,
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state
    )

    print(f"New Session is created with ID: {SESSION_ID}")

    # Create Runner
    runner = Runner(
        agent=qa_agent,
        session_service=session_service,
        app_name=APP_NAME
    )

    ## new message(question) from user to agent
    new_message = types.Content(
        role="user",
        parts=[types.Part(text="What is sayan's favourite game ?")],
    )

    for event in runner.run(
        session_id=SESSION_ID,
        user_id=USER_ID,
        new_message=new_message,
    ):
        if(event.is_final_response()):
            if event.content and event.content.parts:
                print("Agent Final Response: ", event.content.parts[0].text)



if __name__ == "__main__":
    asyncio.run(main())



