from sec_edgar_downloader import Downloader

dl = Downloader(
    "GraphLearningEcon",
    "askagranya1064@gmail.com",
    "data/raw"
)

tickers = ["NVDA", "AMD", "INTC", "AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "UPS", "FDX"]

for ticker in tickers:
    print(f"Downloading {ticker}")
    dl.get("10-K", ticker, limit=3)
    dl.get("10-Q", ticker, limit=3)

# dl.get(
#     "10-K",
#     "AAPL",
#     limit = 5
# )