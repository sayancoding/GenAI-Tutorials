import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel, Field

"""
Define OupenRoute Free LLM model
"""
model = LiteLlm(
    model='openrouter/x-ai/grok-4.1-fast:free',
    api_key = os.getenv("OPENROUTER_API_KEY")
)

class EmailResponse(BaseModel):
    subject: str = Field(description="The subject of the email")
    body: str = Field(description="The body content of the email")
    attachments: list[str] = Field(description="List of attachments for the email")

root_agent = LlmAgent(
    model=model,
    name="email_agent",
    description="An email agent that can help to draft and respond to emails.",
    instruction="""
    Generate email body and subject based on the user's request. Use professional and clear language.
    Make sure to be concise and to the point.
    Suggent some attachedments if necessary.

    Important: Follow below pattern strictly for your response -
    {
        "subject": "<email subject>",
        "body": "<email body>",
        "attachments": ["<attachment1>", "<attachment2>"]  # optional
    }
    """,
    output_schema=EmailResponse,
    output_key="email_response"
)