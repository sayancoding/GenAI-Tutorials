import asyncio

from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService

#========Part 01: Load environment variables from .env file========#
load_dotenv()

#========Part 02: Define database URL for agent state persistence========#
db_url = "sqlite:///agent_data.db"  
session_service = DatabaseSessionService(db_url=db_url)

#========Part 03: Define initial state ========#
initial_state = {
    "user_name": "Sayan maity",
    "reminders": []
}

# async def main():
    
#     # Setup constants
#     APP_NAME = "persistent_agent_app"
#     USER_ID = "user_sayan_123"

#     # ==== Part 04: Check for existing session state ==== #
#     existing_session = session_service.list_sessions(
#         app_name=APP_NAME,
#         user_id=USER_ID
#     )

#     # If existing session found, load it; otherwise, create a new session
#     if existing_session and len(existing_session) > 0:
#         SESSION_ID = existing_session[0].id
#         print(f"Resuming existing session: {SESSION_ID}")
#     else:
#         new_session = session_service.create_session(
#             app_name=APP_NAME,
#             user_id=USER_ID,
#             initial_state=initial_state
#         )
#         SESSION_ID = new_session.id
#         print(f"Created new session: {SESSION_ID}")



# if __name__ == "__main__":
#     asyncio.run(main())