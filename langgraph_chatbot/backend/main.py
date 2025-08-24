from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from langgraph_chatbot.backend.routes import router

app = FastAPI(title="LangGraph Chatbot API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
