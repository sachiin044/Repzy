# streamlit_app.py
import streamlit as st
import requests
import uuid

# ------------------ CONFIG ------------------
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Repo AI", layout="wide")
st.title("🤖 Repzy - Go deeper than the README")

# ------------------ SESSION STATE ------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "repo_indexed" not in st.session_state:
    st.session_state.repo_indexed = False


# ------------------ BACKEND CALL ------------------
def call_backend(endpoint, payload):
    try:
        res = requests.post(f"{BACKEND_URL}{endpoint}", json=payload, timeout=300)
        return res.json()
    except Exception as e:
        st.error(str(e))
        st.stop()


# ------------------ INDEX REPO ------------------
st.header("1️⃣ Index a GitHub Repository")

repo_url = st.text_input("Repository URL")

if st.button("Index Repository"):
    with st.spinner("Indexing..."):
        call_backend("/upload-repo", {"repo_url": repo_url})
    st.session_state.repo_indexed = True
    st.success("Repository indexed")

st.divider()

# ------------------ ASK QUESTION ------------------
st.header("2️⃣ Ask a Question")

question = st.text_input("Your question")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        result = call_backend(
            "/chat",
            {
                "question": question,
                "session_id": st.session_state.session_id
            }
        )

    st.session_state.chat_history.append({
        "question": question,
        "answer": result["answer"],
        "follow_ups": result.get("follow_ups", [])
    })

st.divider()

# ------------------ CHAT ------------------
st.header("💬 Conversation")

for i, chat in enumerate(reversed(st.session_state.chat_history)):
    st.markdown("### 🧑 You")
    st.markdown(chat["question"])

    st.markdown("### 🤖 Repo AI")
    st.markdown(chat["answer"])

    for fq in chat.get("follow_ups", []):
        if st.button(f"➡️ {fq}", key=f"{i}-{fq}"):
            with st.spinner("Thinking..."):
                result = call_backend(
                    "/chat",
                    {
                        "question": fq,
                        "session_id": st.session_state.session_id
                    }
                )

            st.session_state.chat_history.append({
                "question": fq,
                "answer": result["answer"],
                "follow_ups": result.get("follow_ups", [])
            })
            st.rerun()
