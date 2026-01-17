import json
from sentence_transformers import SentenceTransformer
import chromadb

CHROMA_PATH = "./chroma_db"

with open("../rag_pipeline/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client(
    settings=chromadb.Settings(
        persist_directory=CHROMA_PATH
    )
)

collection = client.get_or_create_collection(name="erpnext_code")
# Embed and store all chunks
print("Starting embedding process...")
for i, chunk in enumerate(chunks):
    try:
        embedding = model.encode(chunk).tolist()
        collection.add(
            embeddings=[embedding],
            documents=[chunk],
            ids=[str(i)]
        )
        if (i + 1) % 10 == 0:
            print(f"Embedded {i + 1}/{len(chunks)} chunks")
    except Exception as e:
        print(f"Error embedding chunk {i}: {e}")
        continue

print(f"\nSuccessfully embedded and stored all {len(chunks)} chunks!")
print(f"Collection now contains {collection.count()} documents")