import networkx as nx

graphs_by_period = {}

def add_relationship(period, source, target):
    if period not in graphs_by_period:
        graphs_by_period[period] = nx.DiGraph()
    graphs_by_period[period].add_edge(source, target)