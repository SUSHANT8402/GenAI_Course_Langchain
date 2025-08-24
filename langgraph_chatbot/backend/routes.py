from fastapi import APIRouter
from pydantic import BaseModel
from langgraph_chatbot.chatbot import build_chatbot
from langgraph_chatbot.memory import ChatMemory
from langchain.schema import AIMessage

router = APIRouter()
memory = ChatMemory()
graph = build_chatbot()

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    history = memory.get_history(request.session_id)

    # Run chatbot with past history + new user input
    events = graph.stream({"messages": history + [("user", request.message)]}, stream_mode="values")

    response_text = ""
    for event in events:
        for _, value in event.items():
            for msg in value:
                if isinstance(msg, AIMessage) and msg.content.strip():
                    response_text = msg.content.strip()

    # Save to memory
    memory.add_message(request.session_id, "user", request.message)
    memory.add_message(request.session_id, "ai", response_text)

    return ChatResponse(response=response_text)

@router.get("/health")
def health():
    return {"status": "ok"}
