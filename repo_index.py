import os
import re

PY_FUNC_RE = re.compile(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", re.MULTILINE)
PY_CLASS_RE = re.compile(r"^class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*", re.MULTILINE)

def build_repo_manifest(repo_path: str):
    manifest = {
        "files": [],
        "structure": {}
    }

    for root, _, files in os.walk(repo_path):
        rel_dir = os.path.relpath(root, repo_path)
        manifest["structure"].setdefault(rel_dir, [])

        for file in files:
            manifest["structure"][rel_dir].append(file)
            file_path = os.path.join(root, file)

            entry = {
                "path": os.path.relpath(file_path, repo_path),
                "functions": [],
                "classes": []
            }

            if file.endswith(".py"):
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        entry["functions"] = PY_FUNC_RE.findall(content)
                        entry["classes"] = PY_CLASS_RE.findall(content)
                except:
                    pass

            manifest["files"].append(entry)

    return manifest
