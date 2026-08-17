# src/api/app.py
from contextlib import asynccontextmanager
from datetime import datetime
import json
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.features.similarity import SemanticSymptomSearch
from src.models.predict import DiseasePredictor

# Resolve project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIT_LOG_PATH = PROJECT_ROOT / "data" / "logs" / "audit_sessions.jsonl"
BODY_MAP_PATH = PROJECT_ROOT / "data" / "symptom_body_map.json"

# Global Engine handles
search_engine: Optional[SemanticSymptomSearch] = None
predictor_engine: Optional[DiseasePredictor] = None
body_map_data: Optional[dict] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global search_engine, predictor_engine, body_map_data
    # 1. Ensure log directory exists
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 2. Load ML artifacts & vector search engines
    search_engine = SemanticSymptomSearch()
    predictor_engine = DiseasePredictor()

    # 3. Load symptom body map taxonomy
    if BODY_MAP_PATH.exists():
        with open(BODY_MAP_PATH, "r", encoding="utf-8") as f:
            body_map_data = json.load(f)
    else:
        body_map_data = {}
    yield
    # Teardown logic (if needed on shutdown)


app = FastAPI(title="Sankofa Engine API", version="2.0.0", lifespan=lifespan)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/")
@app.get("/health")
async def health_check():
    """Health-check endpoint for uptime monitors and Render port scanning."""
    return {
        "status": "healthy",
        "service": "Sankofa Engine API",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/symptoms/search")
async def search_symptoms(q: str = Query(..., min_length=2), limit: int = 5):
    """Stage 1: Vector Search Endpoint for Autosuggest UI."""
    if search_engine is None:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
    results = search_engine.search(query=q, top_k=limit)
    return {"query": q, "matches": results}


@app.get("/api/v1/symptoms/by-region/{body_part}")
async def get_symptoms_by_region(body_part: str):
    """Filter symptoms by anatomical body region."""
    if body_map_data is None:
        raise HTTPException(status_code=503, detail="Body map data not initialized")

    normalized_body_part = body_part.lower().strip()
    matched_key = None
    for key in body_map_data.keys():
        if key.lower() == normalized_body_part:
            matched_key = key
            break

    if matched_key is None:
        matched_key = "General"

    return {
        "region": matched_key,
        "symptoms": body_map_data.get(matched_key, [])
    }


@app.post("/api/v1/diagnose", response_model=DiagnosisResponse)
async def run_diagnosis(payload: DiagnosisRequest):
    """Stage 2: Full Diagnostic Prediction with Post-Filtering & Audit Logging."""
    if predictor_engine is None:
        raise HTTPException(status_code=503, detail="Predictor engine not initialized")

    raw_preds = predictor_engine.predict(payload.symptoms, top_k=5)

    # Demographic / Biological Post-Filtering (Rule-based safety layer)
    filtered = []
    for pred in raw_preds:
        disease = pred["disease"].lower()

        # Prevent biological mismatch
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
