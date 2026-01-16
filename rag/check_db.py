import chromadb

client = chromadb.Client(
    settings=chromadb.Settings(
        persist_directory="chroma_db",
        anonymized_telemetry=False
    )
)

collections = client.list_collections()
print([c.name for c in collections])

if collections:
    col = client.get_collection("erpnext_code")
    print("Document count:", col.count())
else:
    print("Document count: 0")
