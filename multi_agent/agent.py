from google.adk.agents import Agent
import requests
import os
from typing import Optional

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_company_overview(symbol: str) -> dict:
    """
    Get comprehensive company information and financial metrics
    
    Args:
        symbol: Stock ticker symbol (e.g., IBM)
    
    Returns:
        dict: Company overview data or error
    """
    if not ALPHA_VANTAGE_API_KEY:
        return {"status": "error", "error": "Missing API key"}
    
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            return {"status": "error", "error": data["Error Message"]}
            
        # Filter key metrics
        key_metrics = {
            "Description": data.get("Description"),
            "Sector": data.get("Sector"),
            "MarketCap": data.get("MarketCapitalization"),
            "PERatio": data.get("PERatio"),
            "ProfitMargin": data.get("ProfitMargin"),
            "52WeekHigh": data.get("52WeekHigh"),
            "52WeekLow": data.get("52WeekLow")
        }
        
        return {
            "status": "success",
            "symbol": symbol,
            "overview": key_metrics
        }
        
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_earnings(symbol: str) -> dict:
    """
    Get annual and quarterly earnings (EPS) data with analyst estimates and surprises
    
    Args:
        symbol: Stock ticker symbol (e.g., IBM)
    
    Returns:
        dict: Earnings data with estimates or error message
    """
    if not ALPHA_VANTAGE_API_KEY:
        return {"status": "error", "error": "Missing API key"}
    
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "EARNINGS",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            return {"status": "error", "error": data["Error Message"]}
            
        # Process annual and quarterly earnings
        annual_earnings = data.get("annualEarnings", [])[:5]  # Last 5 years
        quarterly_earnings = data.get("quarterlyEarnings", [])[:4]  # Last 4 quarters
        
        # Format surprise percentages
        for q in quarterly_earnings:
            if "surprisePercentage" in q:
                q["surprise"] = f"{q['surprisePercentage']}%"
        
        return {
            "status": "success",
            "symbol": symbol,
            "annual_earnings": annual_earnings,
            "quarterly_earnings": quarterly_earnings,
            "metrics": {
                "latest_eps": quarterly_earnings[0]["reportedEPS"] if quarterly_earnings else None
            }
        }
        
    except Exception as e:
        return {"status": "error", "error": str(e)}
    
    
root_agent = Agent(
    name="Financial_analyst_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to give company overviews with key financial metrics."
    ),
    instruction=(
        "You are a helpful AI agent that provides company overviews and earnings information"
    ),
    tools=[get_company_overview, get_earnings],
)