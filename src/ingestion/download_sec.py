from sec_edgar_downloader import Downloader

dl = Downloader(
    "GraphLearningEcon",
    "askagranya1064@gmail.com",
    "data/raw"
)

dl.get(
    "10-K",
    "AAPL",
    limit = 5
)