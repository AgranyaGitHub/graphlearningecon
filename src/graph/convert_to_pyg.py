from torch_geometric.utils import from_networkx
import networkx as nx

G = nx.DiGraph()
G.add_edge("TSMC", "AAPL")
data = from_networkx(G)

print(data)