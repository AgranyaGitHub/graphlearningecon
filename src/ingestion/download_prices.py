import yfinance as yf

tickers = [
    "AAPL",
    "TSM",
    "NVDA",
    "MSFT"
]

data = yf.download(
    tickers,
    start = "2020-01-01",
    end = "2024-01-01"
)

print(data.head())