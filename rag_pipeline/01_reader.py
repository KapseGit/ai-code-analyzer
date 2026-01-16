import os
import json

# Path to ERPNext source code
ERP_PATH = "../erpnext"

files_data = []

for root, dirs, files in os.walk(ERP_PATH):
    for file in files:
        if file.endswith(".py"):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, ERP_PATH)

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()
            except Exception:
                continue

            files_data.append({
                "file": rel_path,
                "language": "python",
                "code": code
            })

print(f"Collected {len(files_data)} Python files")

with open("files_raw.json", "w", encoding="utf-8") as f:
    json.dump(files_data, f, indent=2)

print("Saved files_raw.json")
