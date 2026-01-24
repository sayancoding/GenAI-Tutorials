from google.adk.models.lite_llm import LiteLlm
import os

lite_model = LiteLlm(
    model="ollama_chat/gemma3:4b", 
    api_base="http://localhost:11434")