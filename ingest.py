import os
import git
from repo_index import build_repo_manifest

SUPPORTED_EXT = [".py", ".md", ".txt"]

def clone_repo(repo_url: str, target_dir="repos"):
    os.makedirs(target_dir, exist_ok=True)
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(target_dir, repo_name)

    if not os.path.exists(repo_path):
        git.Repo.clone_from(repo_url, repo_path)

    return repo_path


def read_repo_files(repo_path: str):
    documents = []

    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_EXT):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    documents.append({
                        "text": content,
                        "metadata": {
                            "file": os.path.relpath(full_path, repo_path)
                        }
                    })
                except:
                    pass

    manifest = build_repo_manifest(repo_path)
    return documents, manifest
