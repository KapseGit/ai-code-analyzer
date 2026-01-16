import chromadb

# Load ChromaDB from disk
client = chromadb.Client(
    settings=chromadb.Settings(
        persist_directory="./chroma_db"
    )
)

# SAFE in all Chroma versions
collection = client.get_or_create_collection("erpnext_code")

def search(query, top_k=5):
    return collection.query(
        query_texts=[query],
        n_results=top_k
    )

if __name__ == "__main__":
    query = input("Ask a question about ERPNext code: ")
    results = search(query)

    print("\n--- Retrieved Code Chunks ---\n")

    for i, doc in enumerate(results["documents"][0]):
        print(f"\n### Chunk {i+1}")
        print(doc[:800])  # show first 800 chars
        print("-" * 60)
