import torch
from models.temporal_gnn import TemporalGNN

def train(dataset, num_epochs = 10):
    model = TemporalGNN(num_features = dataset[0].x.shape[1])
    optimizer = torch.optim.Adam(model.parameters() lr = 0.01)
    loss_fn = torch.nn.BCELoss()

    model.train()

    for epoch in range(num_epochs):
        total_loss = 0
        for time, snapshot in enumerate(dataset):
            optimizer.zero_grad()
            out = model(snapshot.x, snapshot.edge_index, snapshot.edge_attr)
            loss = loss_fn(out.squeeze(), snapshot.y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch}: {total_loss}")