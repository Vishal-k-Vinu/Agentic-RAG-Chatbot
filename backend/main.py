from fastapi import FastAPI
from pydantic import BaseModel
from backend.agent import run_agent


app = FastAPI()

class ChatRequest(BaseModel):
    message:str

@app.get("/")
def health():
    return "Agentic RAG is running"


@app.post("/chat")
def chat(request:ChatRequest):
    ans = run_agent(request.message)
    return {
        "question" : request.message,
        "response" : ans
    }
