# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from crew_setup import build_coach_crew, evaluate_with_crew

app = FastAPI(title="Coach Crew Service")

class EvalRequest(BaseModel):
    text_output: str
    confidence: float
    agent_id: str = None
    context: str = None

class EvalResponse(BaseModel):
    pass_fail: bool
    score: float
    stage: str
    feedback: str

# build crew once at startup
CREW = build_coach_crew()

@app.post("/evaluate", response_model=dict)
async def evaluate(request: EvalRequest):
    # if your crew invocations are blocking, run in background loop
    result = await evaluate_with_crew(CREW, output=request.text_output,
                                     confidence=request.confidence,
                                     agent_id=request.agent_id,
                                     context=request.context)
    return result

@app.get("/")
def home():
    return {"status": "coach crew running"}
