import re

from src.graph.company_registry import normalize_company_name, tickers_in_text
from src.graph.extract_entities import extract_organizations_in_span
from src.ingestion.clean_filings import clean_sec_text
from src.ingestion.extract_narrative import extract_narrative_sections
from src.ingestion.section_filter import filter_boilerplate_lines
from src.schemas import Edge, Filing

CONTEXT_WINDOW = 250
SNIPPET_RADIUS = 120

# strong cues --> can use NER + registry fallback in the window
DIRECT_SUPPLIER_PATTERNS = [
    r"\bsupplier\b",
    r"\bmanufacturing partner\b",
    r"\bdepends on\b",
    r"\bsingle source\b",
    r"\boutsourc",
]

# weak cue --> only kept when supply-chain language appears in the same window
THIRD_PARTY_PATTERN = r"\bthird[- ]party\b"
SUPPLY_CHAIN_CUE = re.compile(
    r"\b(supplier|suppliers|manufactur\w*|foundry|wafer|semiconductor|"
    r"fab\b|outsource\w*|foundries)\b",
    re.IGNORECASE,
)

def preprocess_filing_text(text: str) -> str:
    text = filter_boilerplate_lines(text)
    return extract_narrative_sections(clean_sec_text(text))

def _normalize_snippet(text: str, match_span: tuple[int, int]) -> str:
    start = max(0, match_span[0] - SNIPPET_RADIUS)
    end = min(len(text), match_span[1] + SNIPPET_RADIUS)
    snippet = text[start:end].strip()
    return re.sub(r"\s+", " ", snippet)[:500]

def _resolve_orgs_to_tickers(orgs: list[str], focal: str) -> set[str]:
    tickers: set[str] = set()
    for org in orgs:
        ticker = normalize_company_name(org)
        if ticker and ticker != focal:
            tickers.add(ticker)
    return tickers

def _suppliers_in_context(
    context: str,
    focal: str,
    *,
    allow_registry_fallback: bool,
) -> tuple[set[str], str]:
    """
    Returns (supplier_tickers, resolution_method)
    NER-first; registry substring only when allow_registry_fallback = True
    """
    orgs = extract_organizations_in_span(context)
    tickers = _resolve_orgs_to_tickers(orgs, focal)
    ner_tickers = _resolve_orgs_to_tickers(orgs, focal)
    if allow_registry_fallback:
        registry_hits = tickers_in_text(context, exclude=focal)
        combined = ner_tickers | registry_hits
        if not combined:
            return set(), "ner"
        if registry_hits - ner_tickers:
            return combined, "ner+registry"
        return combined, "ner"

    return ner_tickers, "ner"

def _emit_edge(
    edges: list[Edge],
    seen: set[tuple[str, str, str, str, str]],
    *,
    filing: Filing,
    period: str,
    focal: str,
    supplier: str,
    pattern: str,
    resolution: str,
    context_snippet: str,
) -> None:
    key = (period, supplier, focal, pattern, filing.accession)
    if key in seen:
        return
    seen.add(key)
    edges.append(
        Edge(
            period=period,
            source=supplier,
            target=focal,
            relation="supplier",
            focal_ticker=focal,
            pattern=pattern,
            accession=filing.accession,
            filing_path=filing.path,
            context_snippet=context_snippet,
            resolution=resolution,
        )
    )

def extract_edges_from_filing(filing: Filing) -> list[Edge]:
    text = preprocess_filing_text(filing.text)
    focal = filing.ticker
    period = filing.period
    edges: list[Edge] = []
    seen: set[tuple[str, str, str, str, str]] = set()

    for pattern in DIRECT_SUPPLIER_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            start = max(0, match.start() - CONTEXT_WINDOW)
            end = min(len(text), match.end() + CONTEXT_WINDOW)
            context = text[start:end]
            suppliers, resolution = _suppliers_in_context(
                context, focal, allow_registry_fallback=True
            )
            snippet = _normalize_snippet(text, (match.start(), match.end()))
            for supplier in suppliers:
                _emit_edge(
                    edges,
                    seen,
                    filing=filing,
                    period=period,
                    focal=focal,
                    supplier=supplier,
                    pattern=pattern,
                    resolution=resolution,
                    context_snippet=snippet,
                )

    for match in re.finditer(THIRD_PARTY_PATTERN, text, re.IGNORECASE):
        start = max(0, match.start() - CONTEXT_WINDOW)
        end = min(len(text), match.end() + CONTEXT_WINDOW)
        context = text[start:end]
        if not SUPPLY_CHAIN_CUE.search(context):
            continue
        suppliers, resolution = _suppliers_in_context(
            context, focal, allow_registry_fallback=False
        )
        if not suppliers:
            continue
        snippet = _normalize_snippet(text, (match.start(), match.end()))
        for supplier in suppliers:
            _emit_edge(
                edges,
                seen,
                filing=filing,
                period=period,
                focal=focal,
                supplier=supplier,
                pattern=THIRD_PARTY_PATTERN,
                resolution=resolution,
                context_snippet=snippet,
            )

    return edges

def extract_edges_from_filings(filings: list[Filing]) -> list[Edge]:
    all_edges: list[Edge] = []
    for filing in filings:
        all_edges.extend(extract_edges_from_filing(filing))
    return all_edges