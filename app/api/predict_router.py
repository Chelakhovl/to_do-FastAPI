from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.ml_service import ml_service

router = APIRouter(prefix="/predict", tags=["ML"])


class PredictIn(BaseModel):
    """Input schema for prediction."""
    task_description: str = Field(..., min_length=3, max_length=5000)


class PredictOut(BaseModel):
    """Output schema for prediction."""
    priority: Literal["high", "low"]
    confidence: float


@router.post("/", response_model=PredictOut)
def predict_priority(payload: PredictIn):
    """Predict priority (high/low) for a task description."""
    try:
        label, conf = ml_service.predict(payload.task_description)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    return PredictOut(priority=label, confidence=conf)
