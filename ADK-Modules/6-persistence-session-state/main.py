import asyncio
import os
from dotenv import load_dotenv
from google.adk.sessions.sqlite_session_service import SqliteSessionService
from google.adk.runners import Runner

from agents.memory_agent.agent import memory_agent
from utils import call_runner_async

local_db = "./agent_data.db"
session_service = SqliteSessionService(db_path=local_db)

load_dotenv()
print(os.getenv("GOOGLE_API_KEY"))

## Initial Session
initial_state = {
    "user_name" : "Sayan Maity",
    "reminders" : []
}

APP_NAME = "Reminder_Agentic_App"
USER_ID = "sayan_123"



async def main():
    existing_session = await session_service.list_sessions(app_name=APP_NAME,user_id=USER_ID)
    print("====================================")
    if existing_session and len(existing_session.sessions) > 0:
        print(f"Existing Session is using..")
        SESSION_ID = existing_session.sessions[0].id
    else:
        new_session = await session_service.create_session(app_name=APP_NAME,user_id=USER_ID,state=initial_state)
        SESSION_ID = new_session.id
        print(f"New Session is created with Id: {new_session.id}")
    print("====================================")

    runner = Runner(
    app_name=APP_NAME,
    session_service=session_service,
    agent=memory_agent
    )

    print("===========Now Starting conversation with Agent ============")
    print()

    while True:
        user_input = input("👋You : ")

        if user_input.lower() in ['exit','quit']:
            print("----End Conversation----")
            break

        await call_runner_async(runner,USER_ID,SESSION_ID,user_input)

if __name__ == "__main__":
    asyncio.run(main())
    
