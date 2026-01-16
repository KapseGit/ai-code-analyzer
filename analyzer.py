"""
AI Internship – Day 3 Code Analyzer (Audit-Compliant)
====================================================
Extracts a real knowledge graph from ERPNext or any Python legacy system.

Fixes applied:
✔ Handles complex inheritance (ast.Attribute)
✔ Handles import-from properly
✔ Deduplicates entities
✔ Catches parsing errors cleanly
✔ Validates paths
✔ Supports nested methods
✔ Safe output handling
"""

import sys
import ast
import json
from pathlib import Path
from typing import Set


def get_full_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{get_full_name(node.value)}.{node.attr}"
    return None


class CodeAnalyzer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.entities = []
        self.dependencies = []
        self.entity_keys: Set[str] = set()

    # ---------------------------
    def find_python_files(self):
        ignore_dirs = {"__pycache__", ".git", "venv"}
        files = []

        for f in self.root_dir.rglob("*.py"):
            if any(part in ignore_dirs for part in f.parts):
                continue
            files.append(f)

        print(f" Found {len(files)} Python files")
        return files

    # ---------------------------
    def parse_file(self, file_path):
        try:
            try:
                source = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                source = file_path.read_text(errors="ignore")

            tree = ast.parse(source)
            rel_path = str(file_path.relative_to(self.root_dir))
            imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    bases = [get_full_name(b) for b in node.bases if get_full_name(b)]
                    key = f"class:{node.name}:{rel_path}"
                    if key not in self.entity_keys:
                        self.entities.append({
                            "type": "class",
                            "name": node.name,
                            "file": rel_path,
                            "line": node.lineno,
                            "inherits": bases
                        })
                        self.entity_keys.add(key)

                if isinstance(node, ast.FunctionDef):
                    key = f"function:{node.name}:{rel_path}:{node.lineno}"
                    if key not in self.entity_keys:
                        self.entities.append({
                            "type": "function",
                            "name": node.name,
                            "file": rel_path,
                            "line": node.lineno
                        })
                        self.entity_keys.add(key)

                if isinstance(node, ast.Import):
                    for n in node.names:
                        imports.append(n.name)

                if isinstance(node, ast.ImportFrom) and node.module:
                    for n in node.names:
                        imports.append(f"{node.module}.{n.name}")

            if imports:
                self.dependencies.append({
                    "file": rel_path,
                    "imports": list(set(imports))
                })

        except SyntaxError as e:
            print(f" Syntax error in {file_path}: {e}")
        except Exception as e:
            print(f" Failed parsing {file_path}: {e}")

    # ---------------------------
    def analyze(self):
        print("\n Starting AI code analysis...\n")
        files = self.find_python_files()

        for f in files:
            self.parse_file(f)

        print(f"\n Extracted {len(self.entities)} symbols")
        print(f" Dependency files: {len(self.dependencies)}")

    # ---------------------------
    def save(self, out="output"):
        out = Path(out)

        try:
            out.mkdir(exist_ok=True)
        except Exception as e:
            print(f" Cannot create output directory: {e}")
            return

        with open(out / "entities.json", "w", encoding="utf-8") as f:
            json.dump(self.entities, f, indent=2)

        funcs = [e for e in self.entities if e["type"] == "function"]
        clss = [e for e in self.entities if e["type"] == "class"]

        with open(out / "summary.md", "w", encoding="utf-8") as f:
            f.write("# ERPNext Code Analysis\n\n")
            f.write(f"Functions: {len(funcs)}\n")
            f.write(f"Classes: {len(clss)}\n\n")

            f.write("## Sample Functions\n")
            for fn in funcs[:10]:
                f.write(f"- `{fn['name']}` ({fn['file']}:{fn['line']})\n")

            f.write("\n## Sample Classes\n")
            for cl in clss[:10]:
                f.write(f"- `{cl['name']}` ({cl['file']}:{cl['line']})\n")

        with open(out / "dependencies.mermaid", "w", encoding="utf-8") as f:
            f.write("graph TD\n")
            for dep in self.dependencies:
                src = dep["file"].replace("/", "_").replace(".", "_")
                for imp in dep["imports"]:
                    dst = imp.replace(".", "_")
                    f.write(f'{src} --> {dst}\n')

        print("\n Output written to /output")


# ---------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <project_path>")
        sys.exit(1)

    root = Path(sys.argv[1])

    if not root.exists() or not root.is_dir():
        print(" Invalid directory path")
        sys.exit(1)

    analyzer = CodeAnalyzer(root)
    analyzer.analyze()
    analyzer.save()
