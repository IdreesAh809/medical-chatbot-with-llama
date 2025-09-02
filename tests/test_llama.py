import sys
import os

# Add the src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from embeddings import vector_store as vs

# Load index
vs.load_index()

# Check index and chunks
print("Index total vectors:", vs.index.ntotal)
print("Chunks list length:", len(vs.chunks_list))

# Test query
results = vs.query_index("diarrhea treatment", top_k=3)
for i, r in enumerate(results, 1):
    print(f"--- chunk {i} ---")
    print(r[:300].replace("\n", " "))
