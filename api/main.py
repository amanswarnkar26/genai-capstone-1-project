from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from agents import supervisor
from core.logging import logger

app = FastAPI(title="Loan Navigator Agent Suite", version="1.0.0")

class AskRequest(BaseModel):
    query: str = Field(..., description="User question")
    params: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional parameters")

@app.post("/ask")
def ask(req: AskRequest):
    try:
        out = supervisor.handle(req.query, req.params or {})
        return out
    except Exception as e:
        logger.exception("Failed to answer")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/healthz")
def health():
    return {"ok": True}
