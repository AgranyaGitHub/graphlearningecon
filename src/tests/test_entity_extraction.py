from unittest.mock import patch

from src.graph.extract_edges import extract_edges_from_filing, preprocess_filing_text
from src.schemas import Filing


def test_preprocess_strips_markup():
    raw = "<div>Revenue</div>\n\nApple depends on NVIDIA as a key supplier for chips."
    cleaned = preprocess_filing_text(raw)
    assert "<div>" not in cleaned
    assert "supplier" in cleaned.lower()


@patch("src.graph.extract_edges.extract_organizations_in_span")
def test_extract_supplier_edge_to_focal_company(mock_ner):
    mock_ner.return_value = [
        "NVIDIA Corporation",
        "Taiwan Semiconductor Manufacturing Company",
    ]
    text = (
        "Apple Inc. depends on NVIDIA Corporation and Taiwan Semiconductor "
        "Manufacturing Company as primary suppliers for our products."
    ) * 3
    filing = Filing(
        ticker="AAPL",
        form="10-K",
        accession="0000320193-25-000079",
        period="2025-Q2",
        period_source="xbrl",
        path="test",
        text=text,
    )
    edges = extract_edges_from_filing(filing)
    pairs = {(e.source, e.target) for e in edges}
    assert ("NVDA", "AAPL") in pairs or ("TSM", "AAPL") in pairs
