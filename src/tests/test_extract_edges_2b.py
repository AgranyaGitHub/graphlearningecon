from unittest.mock import patch

from src.graph.extract_edges import extract_edges_from_filing, preprocess_filing_text
from src.schemas import Filing


def _filing(text: str, ticker: str = "AAPL") -> Filing:
    return Filing(
        ticker=ticker,
        form="10-K",
        accession="0000320193-25-000079",
        period="2025-Q2",
        period_source="xbrl",
        path="test/path.txt",
        text=text,
    )


@patch("src.graph.extract_edges.extract_organizations_in_span")
def test_direct_supplier_pattern_with_mocked_ner(mock_ner):
    mock_ner.return_value = ["NVIDIA Corporation"]
    text = (
        "Apple Inc. depends on NVIDIA Corporation as a primary supplier for chips. " * 3
    )
    edges = extract_edges_from_filing(_filing(text))
    pairs = {(e.source, e.target) for e in edges}
    assert ("NVDA", "AAPL") in pairs
    assert all(e.context_snippet for e in edges)
    assert all(e.accession for e in edges)


@patch("src.graph.extract_edges.extract_organizations_in_span")
def test_third_party_without_supply_chain_cue_produces_no_edges(mock_ner):
    mock_ner.return_value = ["Microsoft Corporation"]
    text = "We use third party vendors for administrative services. " * 5
    edges = extract_edges_from_filing(_filing(text))
    assert edges == []


@patch("src.graph.extract_edges.extract_organizations_in_span")
def test_third_party_with_supply_chain_cue_and_ner(mock_ner):
    mock_ner.return_value = ["Taiwan Semiconductor Manufacturing Company"]
    text = (
        "We rely on third party foundries, including Taiwan Semiconductor "
        "Manufacturing Company, as suppliers of wafers. " * 3
    )
    edges = extract_edges_from_filing(_filing(text))
    pairs = {(e.source, e.target) for e in edges}
    assert ("TSM", "AAPL") in pairs
    assert all(e.pattern == r"\bthird[- ]party\b" for e in edges)


def test_exhibit_boilerplate_does_not_survive_preprocess():
    raw = (
        "Exhibit 10.1 STOCK OPTION GRANT NOTICE for Microsoft Corporation\n"
        "Item 1. We depend on NVIDIA Corporation as a supplier of chips."
    )
    cleaned = preprocess_filing_text(raw)
    assert "Exhibit" not in cleaned
    assert "supplier" in cleaned.lower()


@patch("src.graph.extract_edges.extract_organizations_in_span")
def test_exhibit_co_mention_does_not_create_edge(mock_ner):
    mock_ner.return_value = ["Microsoft Corporation"]
    text = "Exhibit 10.1 third party agreement with Microsoft Corporation. " * 3
    edges = extract_edges_from_filing(_filing(text))
    assert edges == []
