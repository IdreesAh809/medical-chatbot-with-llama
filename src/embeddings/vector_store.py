import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Global variables
model = SentenceTransformer("all-MiniLM-L6-v2")
index = None
chunks_list = []
dimension = model.get_sentence_embedding_dimension()

# Paths
INDEX_FILE = "data/embeddings/faiss.index"
CHUNKS_FILE = "data/embeddings/chunks.pkl"

def generate_embedding(text: str):
    return model.encode([text])[0]

def create_index(chunks):
    """Create FAISS index from list of text chunks"""
    global index, chunks_list
    chunks_list = chunks
    embeddings = [generate_embedding(chunk) for chunk in chunks]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype="float32"))

    os.makedirs("data/embeddings", exist_ok=True)
    faiss.write_index(index, INDEX_FILE)
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks_list, f)

def load_index():
    """Load FAISS index and chunks from disk"""
    global index, chunks_list
    if os.path.exists(INDEX_FILE) and os.path.exists(CHUNKS_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(CHUNKS_FILE, "rb") as f:
            chunks_list = pickle.load(f)
    else:
        raise FileNotFoundError("Index or chunks file not found. Run create_index first.")

def add_chunks_to_index(new_chunks):
    """Add new chunks to existing FAISS index"""
    global index, chunks_list
    new_embeddings = [generate_embedding(chunk) for chunk in new_chunks]
    index.add(np.array(new_embeddings, dtype="float32"))
    chunks_list.extend(new_chunks)

    # Save updated index
    faiss.write_index(index, INDEX_FILE)
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks_list, f)

def query_index(query, top_k=3):
    """Query FAISS index and return top_k most relevant chunks"""
    global index, chunks_list
    if index is None or not chunks_list:
        raise ValueError("Index not loaded. Call load_index() first.")

    query_embedding = generate_embedding(query).reshape(1, -1)
    D, I = index.search(query_embedding, top_k)
    results = [chunks_list[i] for i in I[0] if i < len(chunks_list)]
    return results
