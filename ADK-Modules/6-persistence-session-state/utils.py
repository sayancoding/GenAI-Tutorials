from google.adk.runners import Runner
from google.genai import types

async def call_runner_async(runner:Runner,user_id:str,session_id:str,user_input:str):
    content = types.Content(role="user",parts=[types.Part(text=user_input)])

    try:
        async for event in runner.run_async(user_id=user_id,session_id=session_id,new_message=content):
            # print(f"==> Event : {event.id} Author: {event.author}")
            if event.is_final_response():
                if (
                event.content
                and event.content.parts
                and hasattr(event.content.parts[0], "text")
                and event.content.parts[0].text
                ):
                    final_response = event.content.parts[0].text.strip()
                    print(f"Agent : {final_response}")

    except Exception as e:
        print(f"Error during agent call : {e}")
    return None