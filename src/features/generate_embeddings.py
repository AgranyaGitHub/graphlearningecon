from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

text = """
Apple depends heavily on
third-party semiconductor suppliers.
"""

embedding = model.encode(text)
print(embedding.shape)