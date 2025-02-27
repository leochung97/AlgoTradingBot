import alpaca_trade_api as tradeapi
import os
import time
import yfinance as yf
import requests
from dotenv import load_dotenv

def get_company_info(ticker):
  """Retrieve company information summary."""
  try:
    # Get company info from Yahoo Finance
    company = yf.Ticker(ticker)
    info = company.info
    
    # Extract relevant information
    name = info.get('longName', 'N/A')
    sector = info.get('sector', 'N/A')
    industry = info.get('industry', 'N/A')
    business_summary = info.get('longBusinessSummary', 'No description available.')
    
    return {
      'name': name,
      'sector': sector,
      'industry': industry,
      'summary': business_summary
    }
  except Exception as e:
    print(f"Error fetching company information: {e}")
    return None

def main():
  # Load environment variables
  load_dotenv()
  
  # Get API credentials
  API_KEY = os.getenv("API_KEY")
  API_SECRET = os.getenv("API_SECRET")
  BASE_URL = os.getenv("BASE_URL")
  
  # Validate environment variables
  if not all([API_KEY, API_SECRET, BASE_URL]):
    print("Error: Missing required environment variables.")
    print("Please check your .env file contains API_KEY, API_SECRET, and BASE_URL.")
    return
  
  # Initialize the Alpaca API
  api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL)
  
  # Prompt for ticker
  ticker = input("Enter stock ticker symbol: ").upper().strip()

  print(f"\n--- {ticker} Stock Information ---\n")

  # Fetch and display company information
  print("Fetching company information...")
  company_info = get_company_info(ticker)
  
  if company_info:
    print(f"\n✓ {company_info['name']} ({ticker})")
    print(f"Sector: {company_info['sector']} | Industry: {company_info['industry']}")
    print("\nBusiness Summary:")
    print("-----------------")
    # Format summary text to wrap at ~80 characters
    words = company_info['summary'].split()
    line_length = 0
    formatted_summary = ""
    
    for word in words:
      if line_length + len(word) + 1 > 80:  # +1 for the space
        formatted_summary += "\n" + word + " "
        line_length = len(word) + 1
      else:
        formatted_summary += word + " "
        line_length += len(word) + 1
    
    print(formatted_summary.strip())
  
  print(f"\nStreaming bid/ask prices for {ticker}. Press Ctrl+C to exit.\n")
  print(f"{'Time':<12} {'Bid':<10} {'Ask':<10} {'Spread':<10}")
  print("-" * 45)
  
  try:
    # Stream data in a loop
    while True:
      # Get current quote
      quote = api.get_latest_quote(ticker)
      
      # Format and display the data
      current_time = time.strftime("%H:%M:%S")
      bid_price = quote.bp if hasattr(quote, 'bp') else "N/A"
      ask_price = quote.ap if hasattr(quote, 'ap') else "N/A"
      
      # Calculate spread if both bid and ask are available
      if isinstance(bid_price, (int, float)) and isinstance(ask_price, (int, float)):
        spread = ask_price - bid_price
        spread_str = f"${spread:.2f}"
      else:
        spread_str = "N/A"
      
      # Print formatted output
      print(f"{current_time:<12} ${bid_price:<9.2f} ${ask_price:<9.2f} {spread_str:<10}")
      
      # Sleep for a second before next update
      time.sleep(0.5)
          
  except KeyboardInterrupt:
    print("\nStream stopped by user.")
  except Exception as e:
    print(f"\nError: {e}")
    if "Not Found" in str(e):
      print(f"The ticker '{ticker}' may not be valid or not supported by Alpaca.")

if __name__ == "__main__":
  main()