from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Any
from agent_logic import AnalyticalAgent
from db_tools import DatabaseTools
import uvicorn
import os

app = FastAPI(title="Agente Analítico de IA - API")

# Configure CORS - Must be before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*", "OPTIONS"],
    allow_headers=["*"],
)

# Create static directory if it doesn't exist
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files to serve charts
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Initialize global instances as None
agent: Optional[AnalyticalAgent] = None
db_tools: Optional[DatabaseTools] = None

@app.on_event("startup")
async def startup_event():
    global agent, db_tools
    print("Initializing Analytical Agent with Charting Support...")
    agent = AnalyticalAgent()
    db_tools = DatabaseTools()
    print("Agent ready.")

class QuestionRequest(BaseModel):
    question: str
    history: Optional[List[dict]] = []

class QuestionResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent is still initializing")
    try:
        answer = await agent.ask(request.question, request.history)
        return QuestionResponse(answer=answer)
    except Exception as e:
        print(f"Error in /ask: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/schema")
async def get_schema():
    if db_tools is None:
        raise HTTPException(status_code=503, detail="Database tools are still initializing")
    try:
        return {"schema": db_tools.get_schema_metadata()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok", "initialized": agent is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
