# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uuid

from ingest import clone_repo, read_repo_files
from embed import create_vector_store
from rag import ask_question
from router import route_question
from followups import generate_followups

load_dotenv()

app = FastAPI(title="RepoLens Backend")

VECTOR_STORE = None
REPO_MANIFEST = None
REPO_PATH = None


# -------------------- MODELS --------------------

class RepoRequest(BaseModel):
    repo_url: str


class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None


# -------------------- HELPERS --------------------

def get_session_id(session_id: str | None) -> str:
    return session_id or str(uuid.uuid4())


def find_file_entry(filename: str):
    for f in REPO_MANIFEST["files"]:
        if f["path"].endswith(filename):
            return f
    return None


def format_code_snippet(code: str, language: str = "python"):
    return f"```{language}\n{code}\n```"


def format_directory_tree(structure: dict):
    lines = []

    for directory in sorted(structure.keys()):
        if directory.startswith(".git"):
            continue

        indent_level = 0 if directory == "." else directory.count(os.sep)
        indent = "│   " * indent_level

        dir_name = "." if directory == "." else directory.split(os.sep)[-1]
        lines.append(f"{indent}📁 {dir_name}/")

        for file in sorted(structure[directory]):
            lines.append(f"{indent}│   📄 {file}")

    return "\n".join(lines)


# -------------------- ROUTES --------------------

@app.post("/upload-repo")
def upload_repo(data: RepoRequest):
    global VECTOR_STORE, REPO_MANIFEST, REPO_PATH

    REPO_PATH = clone_repo(data.repo_url)
    documents, REPO_MANIFEST = read_repo_files(REPO_PATH)
    VECTOR_STORE = create_vector_store(documents)

    return {"status": "Repository indexed successfully"}


@app.post("/chat")
def chat(data: ChatRequest):
    if VECTOR_STORE is None:
        return {"answer": "No repository indexed yet.", "follow_ups": []}

    session_id = get_session_id(data.session_id)
    question = data.question
    q = question.lower()
    route = route_question(q)

    # -------- STRUCTURAL --------
    if route == "STRUCTURAL":
        if "structure" in q or "list files" in q:
            tree = format_directory_tree(REPO_MANIFEST["structure"])
            answer = format_code_snippet(tree, "text")
        elif "how many functions" in q:
            count = sum(len(f["functions"]) for f in REPO_MANIFEST["files"])
            answer = f"Total functions in the repository: {count}"
        elif "functions in" in q and ".py" in q:
            filename = next((w for w in q.split() if w.endswith(".py")), None)
            file_entry = find_file_entry(filename)
            if file_entry:
                answer = (
                    f"File: {filename}\n\n"
                    f"Functions:\n- " + "\n- ".join(file_entry["functions"])
                )
            else:
                answer = "File not found."
        else:
            answer = "Unsupported structural query."

        return {
            "answer": answer,
            "follow_ups": generate_followups(question, answer),
            "session_id": session_id
        }

    # -------- CONTENT --------
    if route == "CONTENT":
        filename = next((w for w in q.split() if w.endswith(".py")), None)
        if filename:
            path = os.path.join(REPO_PATH, filename)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    answer = format_code_snippet(f.read(), "python")
            else:
                answer = "Requested file not found."
        else:
            answer = "No file specified."

        return {
            "answer": answer,
            "follow_ups": generate_followups(question, answer),
            "session_id": session_id
        }

    # -------- SEMANTIC (MEMORY ENABLED) --------
    result = ask_question(VECTOR_STORE, question, session_id)
    result["session_id"] = session_id
    return result
