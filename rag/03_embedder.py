import json
import hashlib
import chromadb

def simple_embedding(text, dim=384):
    """Deterministic local embedding (no network, no ML)"""
    h = hashlib.sha256(text.encode("utf-8")).digest()
    vec = [b / 255 for b in h]
    return (vec * (dim // len(vec) + 1))[:dim]

# Load chunks
with open("../rag_pipeline/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# Local persistent Chroma
client = chromadb.Client(
    settings=chromadb.Settings(
        persist_directory="chroma_db",
        anonymized_telemetry=False,
        allow_reset=True       
    )
)
client.reset()
collection = client.get_or_create_collection("erpnext_code")

for chunk in chunks:
    embedding = simple_embedding(chunk["code"])

    collection.add(
        documents=[chunk["code"]],
        embeddings=[embedding],
        ids=[str(chunk["chunk_id"])],
        metadatas=[{
            "file": chunk["file"],
            "chunk_index": chunk["chunk_index"]
        }]
    )

print("✅ Embeddings stored successfully in ChromaDB (LOCAL MODE)")
client._system.stop()
