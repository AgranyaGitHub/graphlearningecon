import networkx as nx

G = nx.DiGraph()

relationships = [
    ("TSMC", "AAPL"),
    ("Panasonic", "TSLA")
]

edge_features = {
    "dependency_strength": 0.91,
    "shipment_volume": 0.74,
    "relationship_duration": 8.5,
    "geographic_overlap": 0.62
}

for supplier, customer in relationships:
    G.add_edge(
        supplier,
        customer,
        relationship = "supplier",
        timestamp = "2024-Q1",
        **edge_features
    )

print(G.nodes())
print(G.edges())