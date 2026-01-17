from google.adk.agents import Agent
from google.adk.tools.google_search_tool import google_search

from .model import gemini_llm

# constant define for model choose
LLM = gemini_llm

writer_agent = Agent(
    name= "Writer_Agent",
    model=LLM,
    description="Linkedin Post Writting Specialist",
    instruction="""You're very efficient to write linked in post based on user preference.
    - post should be relevant and concise to user preference
    - use google_search tools for latest info about user preference to be more relevant with the topic and pick only top relevant search result.
    - Writting vibe should be professional and simple word use
    - length should not be large
    - don't need to wrap with format, need only plain text
    """,
    tools=[google_search],
    output_key="current_post"
)

def post_char_count_checker(text:str) -> dict:
    """
    Calculates the character count of a given text. 
    Useful for ensuring LinkedIn posts do not exceed the 3000-character limit.
    
    Args:
        text (str): The content of the post to check.
        
    Returns:
        dict: A dictionary containing 'count', 'is_valid', and 'remaining'.
    """
    LIMIT = 3000
    count = len(text)
    return {
        "count": count,
        "limit": LIMIT,
        "is_valid": count <= LIMIT,
        "remaining": LIMIT - count
    }

seo_optimizing_agent = Agent(
    name="SEO_Optimizing_Agent",
    description="You're very good at optimizing the post",
    model=LLM,
    instruction="""Get the post {current_post} and do optimize.
    - use relevant hashtags
    - No emoji
    - redundant word remove
    - check character count using provided tools 
        - if there is more remainig re-generate more content or go for limit_validation check
        - if there is valid count then fine or optimized within limit
    - display the final post content only as output.
    """,
    tools=[post_char_count_checker],
    output_key="current_post"
)

