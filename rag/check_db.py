import chromadb
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(SCRIPT_DIR, "chroma_db")

# Ensure chroma_db directory exists
os.makedirs(CHROMA_PATH, exist_ok=True)

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection("erpnext_code")
print("Collection name:", collection.name)
print("Document count:", collection.count())
