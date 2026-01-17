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
print(f"Stored {len(chunks)} chunks into collection: erpnext_code")