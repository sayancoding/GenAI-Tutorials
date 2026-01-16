from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from .sub_agents import travel_inspiration_agent
from .models import gemini_llm,open_router_llm

from typing import Optional
from datetime import datetime

llm = gemini_llm

def before_agent_callback(callback_context:CallbackContext) -> Optional[types.Content]:
    """hold the sate from context"""
    state = callback_context.state

    """Current timestamp"""
    time = datetime.now()

    if "agent_name" not in state:
        state["agent_name"] = "Travel_Planner_Root_Agent"
    
    if "request_counter" not in state:
        state["request_counter"] = 1
    else:
        state["request_counter"] += 1
    
    state["request_start_time"] = time.isoformat()

    print("==========Agent Execution Started===========")
    print(f"Request Count :: {state['request_counter']}")
    print(f"### {state['agent_name']} ###")
    print(f"Timestamp : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("============Before Agent Callback===========")

    return None

def after_agent_callback(callback_context:CallbackContext) -> Optional[types.Content]:
    """hold the sate from context"""
    state = callback_context.state

    """Current timestamp"""
    time = datetime.now()

    duration = None

    if "request_start_time" in state:
        start_time = datetime.fromisoformat(state["request_start_time"])
        duration = (time - start_time).total_seconds()

    print("==========Agent Execution Completed===========")
    print(f"Request Count :: {state['request_counter']}")
    print(f"### {state['agent_name']} ###")
    if duration is not None:
        print(f"Duration : {duration:.2f}sec.")
    print(f"Timestamp : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("============After Agent Callback===========")

    return None



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
    sub_agents=[travel_inspiration_agent],
    before_agent_callback= before_agent_callback,
    after_agent_callback=after_agent_callback
)