import pickle
from pathlib import Path

import networkx as nx
import pandas as pd

from src.config import EDGES_CSV_PATH, GRAPHS_DIR, GRAPHS_SNAPSHOT_PATH
from src.schemas import Edge


def add_edge(
    graphs: dict[str, nx.DiGraph],
    edge: Edge,
) -> dict[str, nx.DiGraph]:
    if edge.period not in graphs:
        graphs[edge.period] = nx.DiGraph()
    graphs[edge.period].add_edge(
        edge.source,
        edge.target,
        relation=edge.relation,
        focal_ticker=edge.focal_ticker,
        pattern=edge.pattern,
        resolution=edge.resolution,
    )
    return graphs


def build_graphs_from_edges(edges: list[Edge]) -> dict[str, nx.DiGraph]:
    graphs: dict[str, nx.DiGraph] = {}
    for edge in edges:
        add_edge(graphs, edge)
    return graphs


def save_graphs(
    graphs: dict[str, nx.DiGraph],
    snapshot_path: Path | None = None,
    edges_csv_path: Path | None = None,
    edges: list[Edge] | None = None,
) -> None:
    snapshot_path = snapshot_path or GRAPHS_SNAPSHOT_PATH
    edges_csv_path = edges_csv_path or EDGES_CSV_PATH
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)

    with open(snapshot_path, "wb") as handle:
        pickle.dump(graphs, handle)

    if edges is not None:
        rows = [
            {
                "period": e.period,
                "source": e.source,
                "target": e.target,
                "relation": e.relation,
                "focal_ticker": e.focal_ticker,
                "pattern": e.pattern,
                "resolution": e.resolution,
                "accession": e.accession,
                "filing_path": e.filing_path,
                "context_snippet": e.context_snippet,
            }
            for e in edges
        ]
        pd.DataFrame(rows).to_csv(edges_csv_path, index=False)

    print(f"Saved {len(graphs)} period graphs to {snapshot_path}")
    if edges is not None:
        print(f"Saved {len(edges)} edges to {edges_csv_path}")


def load_graphs(snapshot_path: Path | None = None) -> dict[str, nx.DiGraph]:
    snapshot_path = snapshot_path or GRAPHS_SNAPSHOT_PATH
    with open(snapshot_path, "rb") as handle:
        return pickle.load(handle)
