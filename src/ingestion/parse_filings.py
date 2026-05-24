from pathlib import Path

RAW_PATH = Path("data/raw/sec-edgar-filings")

def load_filings():
    filings = []

    for path in RAW_PATH.rglob("*.txt"):
        try:
            text = path.read_text(errors = "ignore")
            filings.append({
                "path": str(path),
                "text": text
            })
        except Exception as e:
            print(f"Error reading path {path}: {e}")
    
    return filings

if __name__ == "__main__":
    filings = load_filings()
    print(f"Loaded {len(filings)} filings")
    print(filings[0]["text"][:1000])