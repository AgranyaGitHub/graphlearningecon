import torch
from torch_geometric_temporal.signal import DynamicGraphTemporalSignal

def build_snapshots(graphs_by_time, features_by_time, labels_by_time):
    edge_indices = []
    edge_attrs = []
    node_features = []
    targets = []

    for t in sorted(graphs_by_time.keys()):
        G = graphs_by_time[t]
        edge_index = torch.tensor(list(G.ed)).t().contiguous()
        edge_attr = torch.ones(edge_index.shape[1], 4)
        x = torch.tensor(features_by_time[t], dtype = torch.float)
        y = torch.tensor(labels_by_time[t], dtype = torch.float)

        edge_indices.append(edge_index)
        edge_attrs.append(edge_attr)
        node_features.append(x)
        targets.append(y)
    
    return DynamicGraphTemporalSignal(
        edge_indices,
        edge_attrs,
        node_features,
        targets
    )