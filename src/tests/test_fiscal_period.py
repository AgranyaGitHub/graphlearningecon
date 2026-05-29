from src.ingestion.fiscal_period import (
    fiscal_period_from_text,
    period_from_accession,
    resolve_filing_period,
)

_XBRL_HEADER = """
<ix:nonNumeric name="dei:DocumentFiscalYearFocus">2025</ix:nonNumeric>
<ix:nonNumeric name="dei:DocumentFiscalPeriodFocus">Q2</ix:nonNumeric>
"""


def test_fiscal_period_from_xbrl_header():
    period = fiscal_period_from_text(_XBRL_HEADER)
    assert period == "2025-Q2"


def test_fiscal_period_fy_only():
    text = '<ix:nonNumeric name="dei:DocumentFiscalYearFocus">2024</ix:nonNumeric>'
    assert fiscal_period_from_text(text) == "2024-FY"


def test_period_from_accession_fallback():
    assert period_from_accession("0000320193-25-000079") == "2025-UNK"


def test_resolve_prefers_xbrl_over_accession():
    period, source = resolve_filing_period(_XBRL_HEADER, "0000320193-24-000079")
    assert period == "2025-Q2"
    assert source == "xbrl"


def test_resolve_falls_back_to_accession():
    period, source = resolve_filing_period("no metadata here", "0000320193-24-000079")
    assert period == "2024-UNK"
    assert source == "accession"
