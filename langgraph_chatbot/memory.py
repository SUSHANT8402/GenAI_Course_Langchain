from typing import Dict, List
from langchain.schema import AIMessage, HumanMessage

class ChatMemory:
    def __init__(self):
        self.store: Dict[str, List] = {}

    def get_history(self, session_id: str):
        return self.store.get(session_id, [])

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.store:
            self.store[session_id] = []
        if role == "user":
            self.store[session_id].append(HumanMessage(content=content))
        else:
            self.store[session_id].append(AIMessage(content=content))

    def clear(self, session_id: str):
        self.store[session_id] = []
