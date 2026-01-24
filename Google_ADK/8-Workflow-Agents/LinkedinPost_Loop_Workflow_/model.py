from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv

load_dotenv()

local_llm = LiteLlm(
    model="ollama_chat/gemma3:4b", 
    api_base="http://localhost:11434"
)

gemini_llm = "gemini-2.0-flash"

open_router_llm = LiteLlm(
    model='openrouter/nvidia/nemotron-nano-12b-v2-vl:free',
    api_key = os.getenv("OPENROUTER_API_KEY")
)