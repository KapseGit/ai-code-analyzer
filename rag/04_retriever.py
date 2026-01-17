import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "./chroma_db"

client = chromadb.Client(
    settings=chromadb.Settings(
        persist_directory=CHROMA_PATH
    )
)

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
