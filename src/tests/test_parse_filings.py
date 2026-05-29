from pathlib import Path

from src.ingestion.fiscal_period import period_from_accession
from src.ingestion.parse_filings import load_filings, parse_filing_path


def test_period_from_accession():
    assert period_from_accession("0000320193-25-000079") == "2025-UNK"


def test_parse_filing_path():
    path = Path(
        "data/raw/sec-edgar-filings/AAPL/10-K/"
        "0000320193-25-000079/full-submission.txt"
    )
    parsed = parse_filing_path(path)
    assert parsed == ("AAPL", "10-K", "0000320193-25-000079")


def test_load_filings_returns_metadata():
    filings = load_filings()
    if not filings:
        return
    sample = filings[0]
    assert sample.ticker
    assert sample.form in {"10-K", "10-Q"}
    assert sample.period
    assert sample.period_source in {"xbrl", "accession"}
