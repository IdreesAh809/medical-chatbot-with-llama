import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from data_loader.pdf_loader import PDFLoader
from embeddings.vector_store import create_index

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        i += chunk_size - overlap
    return chunks

# Load PDF
pdf_path = r"data\raw\WhereThereIsNoDoctor.pdf"  # Use raw string for Windows path
loader = PDFLoader(pdf_path)
text = loader.load()  # This calls the load() method

# Split into chunks
chunks = chunk_text(text)
print(f"Number of chunks created: {len(chunks)}")

# Create FAISS index
create_index(chunks)
print("FAISS index created successfully!")
