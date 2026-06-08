import os
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm

MODEL_NAME = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

model.eval()

def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    
    cls_embedding = outputs.last_hidden_state[:, 0, :]
    
    return cls_embedding.squeeze().numpy()

def chunk_text(text, chunk_size = 1500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def embed_filing(text):
    chunks = chunk_text(text)
    embeddings = []

    for chunk in tqdm(chunks):
        try:
            emb = embed_text(chunk)
            embeddings.append(emb)
        except:
            continue

    return np.mean(embeddings, axis = 0)

def build_node_features(filings):
    rows = []
    for filing in filings:
        node_time_id = f"{filing.ticker}_{filing.period}_{filing.form}"
        embedding = embed_filing(filing.text)
        rows.append({
            "node_time_id": node_time_id,
            "embedding": embedding,
        })
    return rows

def save_features(rows, path = "data/features/finbert_embeddings.npy"):
    os.makedirs(os.path.dirname(path), exist_ok = True)
    
    ids = [r["node_time_id"] for r in rows]
    embeddings = np.array([r["embedding"] for r in rows])

    np.save(path, {
        "ids": ids,
        "embeddings": embeddings
    })

    print(f"Saved embeddings to {path}")

if __name__ == "__main__":
    from src.ingestion.parse_filings import load_filings

    filings = load_filings()
    rows = build_node_features(filings)
    save_features(rows)