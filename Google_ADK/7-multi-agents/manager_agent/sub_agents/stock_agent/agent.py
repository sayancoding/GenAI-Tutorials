from google.adk.agents import Agent

import yfinance as yf
import datetime
from google.adk.models.lite_llm import LiteLlm
import os

lite_model = LiteLlm(
    model="ollama_chat/gemma3:4b", 
    api_base="http://localhost:11434"
)

def get_stock_price(ticker: str) -> dict:
    """Retrieves current stock price and saves to session state."""
    print(f"--- Tool: get_stock_price called for {ticker} ---")

    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)
        current_price = stock.info.get("currentPrice")

        if current_price is None:
            return {
                "status": "error",
                "error_message": f"Could not fetch price for {ticker}",
            }

        # Get current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "status": "success",
            "ticker": ticker,
            "price": current_price,
            "timestamp": current_time,
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching stock data: {str(e)}",
        }


# Create the root agent
stock_analyst = Agent(
    name="stock_agent",
    model=lite_model,
    description="An agent that can look up stock prices and track them over time.",
    instruction="""
    You are a helpful stock market assistant that helps users track their stocks of interest with help of tools    
    Example response format:
    "Here are the current prices for your stocks:
    - GOOG: $175.34 (updated at 2024-04-21 16:30:00)
    """,
    tools=[get_stock_price],
)