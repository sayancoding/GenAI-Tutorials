from google.adk.agents import Agent
from google.adk.tools.google_search_tool import google_search
from google.adk.tools.exit_loop_tool import exit_loop
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool

from .model import gemini_llm
from typing import Dict,Optional,Any
# constant define for model choose
LLM = gemini_llm

writer_agent = Agent(
    name= "Writer_Agent",
    model=LLM,
    description="Linkedin Post Writting Specialist",
    instruction="""You're very efficient to write linked in post based on user preference.
    - post should be relevant and concise to user preference
    - always generate one post not multiple option
    - use google_search tools for latest info about user-preference topic and pick only top relevant search result.
    - Writting vibe should be professional and simple word use
    - don't need to wrap with format, need only plain text
    - generate long paragraph

    IMPORTANT FEEDBACK FROM PREVIOUS ATTEMPT:
    - Current Character Count: {last_count?}
    - Characters to remove: {chars_over?}
    If 'chars_over' is greater than 0, rewrite the post to be more concise 
    while keeping the same core message.
    """,
    tools=[google_search],
    output_key="current_post"
)

seo_optimizing_agent = Agent(
    name="SEO_Optimizing_Agent",
    description="You're very good at optimizing the post",
    model=LLM,
    instruction="""Get the post {current_post} and do optimize.
    - use relevant hashtags
    - No emoji
    - redundant word remove
    """,
    output_key="current_post"
)

def after_tool_callback(
        tool: BaseTool,
        args: Dict[str, Any], # argument passed by agent
        tool_context: ToolContext, # The system context (where you set state)
        tool_response: Optional[Dict] # output of function-tool
    )-> Optional[Dict]:
    
    if tool_response is None:
        return None

    limit = 1000
    current_count = tool_response.get("count",0)
    tool_context.state["last_count"] = current_count
    tool_context.state["chars_over"] = max(0, current_count - limit)
    if "text" in args:
        tool_context.state["current_post"] = args["text"]
    return None

def post_char_count_checker(text:str) -> dict:
    """Calculates character count to ensure it's under the 3000 limit."""
    limit = 1000
    count = len(text)

    return {
        "count": count,
        "is_valid": count <= limit,
        "feedback": f"Too long! Please cut {count - limit} characters." if count > limit else "Perfect length."
    }

critic_agent = Agent(
    name="Critic_Agent",
    model=LLM,
    instruction="""
    1. Use 'post_char_count_checker' on the latest {current_post}.
    2. If it is valid (under 1000 chars):
       - Call 'exit_loop'.
       - IMPORTANT: Your final response MUST be ONLY the text from {current_post}.
    3. If invalid, explain the errors.
    """,
    output_key="current_post",
    tools=[post_char_count_checker, exit_loop],
    after_tool_callback=after_tool_callback
)

