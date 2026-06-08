from collections import Counter

from src.graph.company_registry import known_tickers
from src.schemas import Edge

VALID_RELATIONS = {"supplier"}
VALID_RESOLUTIONS = {"ner", "ner+registry"}

def validate_edge(edge: Edge) -> list[str]:
    """
    Return human-readable validation errors for a single edge ("empty" = valid)
    """
    errors: list[str] = []
    known = known_tickers()

    if edge.source == edge.target:
        errors.append("self-loop")
    if edge.source not in known:
        errors.append(f"unknown source ticker: {edge.source}")
    if edge.target not in known:
        errors.append(f"unknown target ticker: {edge.target}")
    if edge.focal_ticker != edge.target:
        errors.append("focal_ticker must equal target")
    if edge.relation not in VALID_RELATIONS:
        errors.append(f"invalid relation: {edge.relation}")
    if edge.resolution not in VALID_RESOLUTIONS:
        errors.append(f"invalid resolution: {edge.resolution}")
    if not edge.context_snippet.strip():
        errors.append("empty context_snippet")
    if len(edge.context_snippet) > 600:
        errors.append("context_snippet too long")
    return errors

def validate_edges(edges: list[Edge]) -> list[tuple[Edge, list[str]]]:
    return [(edge, validate_edge(edge)) for edge in edges if validate_edge(edge)]

def dedupe_edges(edges: list[Edge]) -> list[Edge]:
    """
    Global dedup on (period, source, target, relation)
    Keeps first edge --> merges lineage into filing_path field metadata via semicolon when duplicate filings agree on the same relationship
    """
    buckets: dict[tuple[str, str, str, str], Edge] = {}
    accessions: dict[tuple[str, str, str, str], list[str]] = {}

    for edge in edges:
        key = (edge.period, edge.source, edge.target, edge.relation)
        if key not in buckets:
            buckets[key] = edge
            accessions[key] = [edge.accession]
            continue
        if edge.accession not in accessions[key]:
            accessions[key].append(edge.accession)

    deduped: list[Edge] = []
    for key, edge in buckets.items():
        merged_accession = ";".join(sorted(accessions[key]))
        if merged_accession != edge.accession:
            edge = Edge(
                period=edge.period,
                source=edge.source,
                target=edge.target,
                relation=edge.relation,
                focal_ticker=edge.focal_ticker,
                pattern=edge.pattern,
                accession=merged_accession,
                filing_path=edge.filing_path,
                context_snippet=edge.context_snippet,
                resolution=edge.resolution,
            )
        deduped.append(edge)

    return deduped

def corpus_report(edges: list[Edge]) -> dict:
    """
    Summary stats for internal validation after extraction
    """
    invalid = validate_edges(edges)
    return {
        "n_edges": len(edges),
        "n_invalid": len(invalid),
        "focal_tickers": dict(Counter(e.focal_ticker for e in edges)),
        "patterns": dict(Counter(e.pattern for e in edges)),
        "resolutions": dict(Counter(e.resolution for e in edges)),
        "periods": dict(Counter(e.period for e in edges)),
        "unique_triples": len(
            {(e.period, e.source, e.target) for e in edges}
        ),
    }

def assert_corpus_valid(edges: list[Edge], max_invalid: int = 0) -> dict:
    """
    Raises ValueError if validation fails
    Called at end of build pipeline for internal QA
    """
    report = corpus_report(edges)
    invalid = validate_edges(edges)
    if len(invalid) > max_invalid:
        sample = invalid[0]
        raise ValueError(
            f"Edge validation failed: {len(invalid)} invalid edges"
            f"Example: {sample[1]} edge={sample[0]}"
        )
    return report