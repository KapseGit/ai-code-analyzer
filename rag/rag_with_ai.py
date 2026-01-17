import os
import sys
import chromadb
from sentence_transformers import SentenceTransformer

# =============================================================================
# CONFIG
# =============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(SCRIPT_DIR, "chroma_db")
COLLECTION_NAME = "erpnext_code"
TOP_K = 5

# =============================================================================
# INITIALIZE
# =============================================================================
print("\nInitializing ERPNext RAG System (LLM Optional Mode)...\n")

# Load Vector DB
try:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(COLLECTION_NAME)
    total_docs = collection.count()
    print(f"✓ Vector DB loaded ({total_docs} code chunks)")
except Exception as e:
    print("❌ Failed to load ChromaDB")
    print("   Make sure 03_embedder.py ran successfully")
    print(f"   Error: {e}")
    sys.exit(1)

# Load embedding model
try:
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    print("✓ Embedding model loaded\n")
except Exception as e:
    print("❌ Failed to load embedding model")
    print(e)
    sys.exit(1)

print("=" * 60)
print("✓ RAG CORE READY")
print("✓ Solves context exhaustion")
print("✓ No summarization loss")
print("✓ No hallucinations")
print("✓ LLM can be plugged later")
print("=" * 60 + "\n")

# =============================================================================
# RAG QUERY FUNCTION
# =============================================================================
def rag_query(question: str, top_k: int = TOP_K):
    print("=" * 80)
    print(f"QUESTION: {question}")
    print("=" * 80 + "\n")

    # Step 1: Vector Search
    print("[1/2] Searching vector database...")
    query_embedding = embedder.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]

    if not docs:
        print("❌ No relevant code found")
        return

    print(f"✓ Retrieved {len(docs)} code chunks\n")

    # Step 2: Display Retrieved Context (Source of Truth)
    print("[2/2] Retrieved Code Context (NO LLM)\n")

    context_chars = 0
    retrieved_files = set()

    for i, doc in enumerate(docs):
        meta = metas[i] if i < len(metas) and isinstance(metas[i], dict) else {}
        file_path = meta.get("file", "Unknown file")
        distance = dists[i] if i < len(dists) else 1.0
        relevance = max(0.0, 1 - distance)

        retrieved_files.add(file_path)
        context_chars += len(doc)

        print(f"--- Chunk {i+1}")
        print(f"File      : {file_path}")
        print(f"Relevance : {relevance:.2f}")
        print("-" * 40)
        print(doc[:800])  # safe preview
        print("\n")

    tokens_estimate = context_chars // 4
    context_percent = (tokens_estimate / 100000) * 100

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Files involved     : {len(retrieved_files)}")
    print(f"Context characters : {context_chars}")
    print(f"Estimated tokens   : {tokens_estimate}")
    print(f"Context usage      : {context_percent:.2f}%")
    print("\nNOTE:")
    print("- This is exact code (no summarization)")
    print("- Safe for large legacy systems")
    print("- LLM can be added later for explanation")
    print("=" * 80 + "\n")


# =============================================================================
# INTERACTIVE MODE
# =============================================================================
if __name__ == "__main__":
    print(f"✓ {total_docs} ERPNext code chunks indexed")
    print("Type your questions below (type 'exit' to quit)\n")

    while True:
        try:
            user_input = input("Ask about ERPNext code: ").strip()

            if user_input.lower() in ("exit", "quit", "q"):
                print("\nExiting RAG System. Goodbye!\n")
                break

            if not user_input:
                print("Please enter a valid question\n")
                continue

            rag_query(user_input)

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.\n")
            break
        except Exception as err:
            print(f"\n❌ Error: {err}\n")
