import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edge("TSM", "AAPL")
G.add_edge("NVDA", "TSM")
G.add_edge("AAPL", "MSFT")

nx.draw(G, with_labels = True)

plt.show()