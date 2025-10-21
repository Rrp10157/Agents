# ============================================
# main.py
# ============================================
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from crew_setup import generate_and_evaluate, evaluate_with_crew, batch_evaluate

app = FastAPI(title="Coach Crew Service - Complete Q&A with Evaluation")

class QueryRequest(BaseModel):
    """Request for complete flow: query → answer → evaluation"""
    query: str
    context: Optional[str] = None
    agent_id: Optional[str] = None

class EvalRequest(BaseModel):
    """Request for evaluation only (if you already have an answer)"""
    text_output: str
    confidence: float
    agent_id: Optional[str] = None
    context: Optional[str] = None

class BatchEvalRequest(BaseModel):
    outputs: List[dict]
    agent_id: Optional[str] = None

@app.post("/ask")
async def ask_question(request: QueryRequest):
    """
    Complete flow: Accept user question → Generate answer → Evaluate
    This is what you want for end-to-end Q&A with evaluation
    """
    try:
        result = await generate_and_evaluate(
            user_query=request.query,
            context=request.context,
            agent_id=request.agent_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate")
async def evaluate(request: EvalRequest):
    """Evaluate an already-generated answer (evaluation only)"""
    try:
        result = await evaluate_with_crew(
            output=request.text_output,
            confidence=request.confidence,
            agent_id=request.agent_id,
            context=request.context
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-evaluate")
async def batch_eval(request: BatchEvalRequest):
    """Batch evaluation endpoint with aggregation"""
    try:
        result = await batch_evaluate(
            outputs=request.outputs,
            agent_id=request.agent_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {
        "status": "Coach Crew Service Running",
        "description": "Complete Q&A system with AI evaluation",
        "endpoints": {
            "/ask": "POST - Ask question → Get answer + evaluation (MAIN ENDPOINT)",
            "/evaluate": "POST - Evaluate existing answer only",
            "/batch-evaluate": "POST - Batch evaluation with aggregation",
            "/health": "GET - Health check"
        },
        "example_usage": {
            "endpoint": "/ask",
            "method": "POST",
            "body": {
                "query": "What is the capital of France?",
                "context": "Geography question",
                "agent_id": "user_123"
            }
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "architecture_compliant": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )