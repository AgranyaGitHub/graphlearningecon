import torch
import torch.nn.functional as F
from torch_geometric_temporal.nn.recurrent import EvolveGCNH

class TemporalGNN(torch.nn.Module):
    def __init__(self, num_features):
        super().__init__()

        self.recurrent = EvolveGCNH(num_features, 32)
        self.linear = torch.nn.Linear(32, 1)
    
    def forward(self, x, edge_index, edge_weight):
        h = self.recurrent(x, edge_index, edge_weight)
        out = self.linear(h)
        return torch.sigmoid(out)