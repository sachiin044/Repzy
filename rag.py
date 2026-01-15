# rag.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from followups import generate_followups
from memory import get_session_history


PROMPT = """
You are a senior software engineer.

Conversation so far:
-------------------
{history}
-------------------

Repository Context:
-------------------
{context}
-------------------

Question:
{question}

Answer clearly, technically, and concisely.
"""


def _format_history(history):
    lines = []
    for msg in history.messages:
        role = "User" if msg.type == "human" else "Assistant"
        lines.append(f"{role}: {msg.content}")
    return "\n".join(lines)


def ask_question(vectorstore, question: str, session_id: str):
    # Retrieve memory
    history = get_session_history(session_id)

    # Vector search
    docs = vectorstore.similarity_search(question, k=20)
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = PromptTemplate(
        input_variables=["context", "question", "history"],
        template=PROMPT
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    )

    history_text = _format_history(history)

    answer = llm.invoke(
        prompt.format(
            context=context,
            question=question,
            history=history_text
        )
    ).content

    # 🔁 Update memory
    history.add_user_message(question)
    history.add_ai_message(answer)

    followups = generate_followups(question, answer)

    return {
        "answer": answer,
        "follow_ups": followups
    }
