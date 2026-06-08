import re
from functools import lru_cache
import pandas as pd
from rapidfuzz import process

from src.config import REGISTRY_PATH

@lru_cache(maxsize=1)
def _load_registry() -> tuple[dict[str, str], dict[str, str], list[str]]:
    registry = pd.read_csv(REGISTRY_PATH)
    ticker_to_name = dict(zip(registry["ticker"], registry["name"]))
    name_to_ticker = {name.lower(): ticker for ticker, name in ticker_to_name.items()}
    company_names = list(name_to_ticker.keys())
    return ticker_to_name, name_to_ticker, company_names

def known_tickers() -> set[str]:
    ticker_to_name, _, _ = _load_registry()
    return set(ticker_to_name)

def normalize_company_name(name: str) -> str | None:
    _, name_to_ticker, company_names = _load_registry()
    name = name.lower().strip()

    if name in name_to_ticker:
        return name_to_ticker[name]

    match = process.extractOne(name, company_names)
    if match:
        matched_name, score, _ = match
        if score > 85:
            return name_to_ticker[matched_name]

    return None

def tickers_in_text(text: str, exclude: str | None = None) -> set[str]:
    ticker_to_name, name_to_ticker, _ = _load_registry()
    text_lower = text.lower()
    found: set[str] = set()

    for name, ticker in name_to_ticker.items():
        if ticker == exclude:
            continue
        if name in text_lower:
            found.add(ticker)

    for ticker in ticker_to_name:
        if ticker == exclude:
            continue
        pattern = rf"\b{re.escape(ticker.lower())}\b"
        if re.search(pattern, text_lower):
            found.add(ticker)

    return found