from src.graph.edge_validation import assert_corpus_valid, corpus_report, dedupe_edges
from src.graph.extract_edges import extract_edges_from_filings
from src.graph.temporal_graph import build_graphs_from_edges, save_graphs
from src.ingestion.parse_filings import load_filings
from src.schemas import Edge, Filing

def build_from_filings(filings: list[Filing]) -> tuple[dict, list[Edge], dict]:
    edges = dedupe_edges(extract_edges_from_filings(filings))
    report = assert_corpus_valid(edges)
    graphs = build_graphs_from_edges(edges)
    return graphs, edges, report

def build_and_save() -> tuple[dict, list[Edge], dict]:
    filings = load_filings()
    graphs, edges, report = build_from_filings(filings)
    save_graphs(graphs, edges=edges)
    return graphs, edges, report

if __name__ == "__main__":
    graphs, edges, report = build_and_save()
    print(corpus_report(edges))
    print(f"Extracted {len(edges)} deduped edges across {len(graphs)} periods")
    for period in sorted(graphs):
        graph = graphs[period]
        print(f"  {period}: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")