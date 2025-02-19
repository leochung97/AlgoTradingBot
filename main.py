# Boiler plate starter code for Alpaca Crypto API
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

client = CryptoHistoricalDataClient()

request_params = CryptoBarsRequest(
  symbol_or_symbols=["BTC/USD"],
  timeframe=TimeFrame.Day,
  start="2025-02-19"
)

bars = client.get_crypto_bars(request_params)
print(bars)