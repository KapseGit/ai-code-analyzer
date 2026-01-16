import json

INPUT_FILE = "files_raw.json"
OUTPUT_FILE = "chunks.json"

MAX_LINES_PER_CHUNK = 120  # safe size for LLM context

def chunk_code(code, max_lines):
    lines = code.splitlines()
    chunks = []

    for i in range(0, len(lines), max_lines):
        chunk = "\n".join(lines[i:i + max_lines])
        chunks.append(chunk)

    return chunks

# Load raw files
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    files = json.load(f)

all_chunks = []
chunk_id = 0

for file in files:
    code_chunks = chunk_code(file["code"], MAX_LINES_PER_CHUNK)

    for index, chunk in enumerate(code_chunks):
        all_chunks.append({
            "chunk_id": chunk_id,
            "file": file["file"],
            "language": file["language"],
            "chunk_index": index,
            "code": chunk
        })
        chunk_id += 1

print(f"Created {len(all_chunks)} chunks")

# Save chunks
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2)

print(f"Saved {OUTPUT_FILE}")
