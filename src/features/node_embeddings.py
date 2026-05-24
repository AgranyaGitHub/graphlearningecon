from node2vec import Node2Vec

node2vec = Node2Vec(
    G, 
    dimensions = 64, 
    walk_length = 20,
    num_walks = 200
)

model = node2vec.fit()
embedding = model.wv["AAPL"]

print(embedding.shape)