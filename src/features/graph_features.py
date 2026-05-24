import networkx as nx

def compute_graph_features(G):
    pagerank = nx.pagerank(G)
    degree = dict(G.degree())
    betweenness = nx.betweenness_centrality(G)

    return {
        "pagerank": pagerank,
        "degree": degree,
        "betweenness": betweenness
    }