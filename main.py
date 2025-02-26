import alpaca_trade_api as tradeapi
import time
import pandas as pd
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables [Paper Account]
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL")

if not all ([API_KEY, API_SECRET, BASE_URL]):
  raise ValueError("Missing required environment variables - check your .env file.")

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")

# Check if the market is open
try:
  clock = api.get_clock()
  print(f"The market is {'open' if clock.is_open else 'closed'}")
  print(f"Next market open: {clock.next_open}")
  print(f"Next market close: {clock.next_close}")
except Exception as e:
  print(f"Error connecting to Alpaca API: {e}")
  print(f"Check that your BASE_URL is correct: {BASE_URL}")