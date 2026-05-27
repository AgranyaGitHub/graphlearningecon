from pathlib import Path
from graph.extract_entities import extract_organizations

path = next(Path("data/raw/sec-edgar_filings").rglob("*.txt"))
print(f"\nUsing filing:\n{path}\n")

text = path.read_text(errors="ignore")
orgs = extract_organizations(text)
print(orgs[:20])