import chromadb
import os
from sentence_transformers import SentenceTransformer

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(SCRIPT_DIR, "chroma_db")

# Ensure chroma_db directory exists
os.makedirs(CHROMA_PATH, exist_ok=True)

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection("erpnext_code")
model = SentenceTransformer("all-MiniLM-L6-v2")

query = input("Ask a question about ERPNext code: ")
query_embedding = model.encode(query)
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

print("\n--- Retrieved Code Chunks ---\n")
for doc in results["documents"][0]:
    print(doc[:500])
    print("-" * 60)
