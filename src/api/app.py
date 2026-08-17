# src/api/app.py
from datetime import datetime
import json
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.features.similarity import SemanticSymptomSearch
from src.models.predict import DiseasePredictor

app = FastAPI(title="Sankofa Engine API", version="2.0.0")

# Enable CORS for local Nuxt / Netlify frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Engines (loaded once at startup)
search_engine: Optional[SemanticSymptomSearch] = None
predictor_engine: Optional[DiseasePredictor] = None
AUDIT_LOG_PATH = Path("data/logs/audit_sessions.jsonl")


@app.on_event("startup")
def startup_event():
    global search_engine, predictor_engine
    search_engine = SemanticSymptomSearch()
    predictor_engine = DiseasePredictor()
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


# --- Request / Response Schemas ---
class PatientMetadata(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=120)
    sex: str = Field(..., description="M, F, or OTHER")
    bmi: Optional[float] = None


class DiagnosisRequest(BaseModel):
    symptoms: List[str] = Field(..., min_items=1)
    metadata: PatientMetadata


class PredictionItem(BaseModel):
    disease: str
    probability: float
    urgency: str
    recommendation: str


class DiagnosisResponse(BaseModel):
    extracted_symptoms: List[str]
    predictions: List[PredictionItem]
    status: str
    disclaimer: str


# --- Endpoints ---


@app.get("/api/v1/symptoms/search")
async def search_symptoms(q: str = Query(..., min_length=2), limit: int = 5):
    """Stage 1: Vector Search Endpoint for Autosuggest UI."""
    results = search_engine.search(query=q, top_k=limit)
    return {"query": q, "matches": results}


@app.post("/api/v1/diagnose", response_model=DiagnosisResponse)
async def run_diagnosis(payload: DiagnosisRequest):
    """Stage 2: Full Diagnostic Prediction with Post-Filtering & Audit Logging."""
    raw_preds = predictor_engine.predict(payload.symptoms, top_k=5)

    # Demographic / Biological Post-Filtering (Rule-based safety layer)
    filtered = []
    for pred in raw_preds:
        disease = pred["disease"].lower()

        # Example biological rule: prevent biological mismatch
        if payload.metadata.sex == "M" and any(
            w in disease for w in ["ovarian", "cervical", "uterine", "pregnancy"]
        ):
            continue
        if payload.metadata.sex == "F" and any(
            w in disease for w in ["prostate", "testicular"]
        ):
            continue

        filtered.append(
            PredictionItem(
                disease=pred["disease"].title(),
                probability=pred["probability"],
                urgency="Urgent" if pred["probability"] > 0.70 else "Routine",
                recommendation="Consult a qualified clinician for verification.",
            )
        )

    final_predictions = filtered[:3]

    # Session Audit Logging for Ethics Stage
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "input_symptoms": payload.symptoms,
        "patient_metadata": payload.metadata.dict(),
        "predictions": [p.dict() for p in final_predictions],
    }
    with open(AUDIT_LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return DiagnosisResponse(
        extracted_symptoms=payload.symptoms,
        predictions=final_predictions,
        status="SUCCESS" if final_predictions else "NO_MATCH",
        disclaimer="DISCLAIMER: Sankofa is an academic prototype and not a certified diagnostic device.",
    )
