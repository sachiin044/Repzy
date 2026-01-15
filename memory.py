# memory.py
from langchain_core.chat_history import InMemoryChatMessageHistory
from typing import Dict

# In-process memory store
_MEMORY_STORE: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """
    Returns chat history for a session.
    Creates a new one if it does not exist.
    """
    if session_id not in _MEMORY_STORE:
        _MEMORY_STORE[session_id] = InMemoryChatMessageHistory()
    return _MEMORY_STORE[session_id]
