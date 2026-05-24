import pandas as pd
from rapidfuzz import process

registry = pd.read_csv("data/company_registry.csv")
ticker_to_name = dict(zip(registry["ticker"], registry["name"]))
name_to_ticker = {v.lower(): k for k, v in ticker_to_name.items()}

company_names = list(name_to_ticker.keys())

# print(name_to_ticker)

def normalize_company_name(name):
    name = name.lower().strip()
    
    # exact match
    if name in name_to_ticker:
        return name_to_ticker[name]
    
    # fuzzy match --> entity resolution
    match = process.extractOne(name, company_names)
    if match:
        matched_name, score, _ = match
        if score > 85:
            return name_to_ticker[matched_name]
    
    return None