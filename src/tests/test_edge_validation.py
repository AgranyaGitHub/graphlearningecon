from src.graph.edge_validation import corpus_report, dedupe_edges, validate_edge
from src.schemas import Edge


def _edge(**overrides) -> Edge:
    base = dict(
        period="2025-Q2",
        source="NVDA",
        target="AAPL",
        relation="supplier",
        focal_ticker="AAPL",
        pattern=r"\bsupplier\b",
        accession="0001",
        filing_path="/tmp/a.txt",
        context_snippet="Apple depends on NVIDIA as a supplier.",
        resolution="ner",
    )
    base.update(overrides)
    return Edge(**base)


def test_validate_edge_accepts_well_formed_edge():
    assert validate_edge(_edge()) == []


def test_validate_edge_rejects_self_loop():
    errors = validate_edge(_edge(source="AAPL", target="AAPL", focal_ticker="AAPL"))
    assert "self-loop" in errors


def test_dedupe_merges_accessions():
    e1 = _edge(accession="acc-a")
    e2 = _edge(accession="acc-b", context_snippet="other")
    deduped = dedupe_edges([e1, e2])
    assert len(deduped) == 1
    assert "acc-a" in deduped[0].accession and "acc-b" in deduped[0].accession


def test_corpus_report_counts():
    report = corpus_report([_edge(), _edge(source="TSM")])
    assert report["n_edges"] == 2
    assert report["unique_triples"] == 2
