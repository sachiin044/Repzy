# embed.py

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def create_vector_store(documents):
    """
    Create a FAISS vector store from repository documents.

    - Uses CPU-only embeddings (prevents PyTorch meta tensor crash)
    - Chunks code/text safely for RAG
    - Stable for Windows, local dev, and deployment
    """

    # -------------------- TEXT SPLITTING --------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    texts = []
    metadatas = []

    for doc in documents:
        chunks = splitter.split_text(doc["text"])
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append(doc["metadata"])

    # -------------------- EMBEDDINGS (CPU SAFE) --------------------
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={
            "device": "cpu"   # 🔒 critical: avoids meta tensor crash
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    # -------------------- VECTOR STORE --------------------
    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    return vectorstore
