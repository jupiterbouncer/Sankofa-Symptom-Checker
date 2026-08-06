import os
import json
import datetime
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List

from src.api.schemas import (
    PatientMetadata,
    DiagnosisRequest,
    DiseasePrediction,
    DiagnosisResponse,
    SymptomItem
)
from src.api import mock_data

# Optional ML libraries import
try:
    import joblib
    HAS_ML_LIBS = True
except ImportError:
    HAS_ML_LIBS = False

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

# Setup FastAPI App
app = FastAPI(
    title="Sankofa Symptom Checker API",
    description="Decoupled API backend for Ashesi Symptom Checker",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
DATA_LOGS_DIR = "/home/onkhida/Desktop/onkbuilds/Sankofa-Symptom-Checker/data/logs"
AUDIT_LOG_PATH = os.path.join(DATA_LOGS_DIR, "audit_sessions.jsonl")
EMBEDDINGS_PATH = "/home/onkhida/Desktop/onkbuilds/Sankofa-Symptom-Checker/data/embeddings/symptom_vectors.joblib"
MODEL_PATH = "/home/onkhida/Desktop/onkbuilds/Sankofa-Symptom-Checker/model/random_forest.pkl"
ENCODER_PATH = "/home/onkhida/Desktop/onkbuilds/Sankofa-Symptom-Checker/model/label_encoder.pkl"
COLUMNS_PATH = "/home/onkhida/Desktop/onkbuilds/Sankofa-Symptom-Checker/model/feature_columns.json"

# Load SentenceTransformer and Embeddings if available
sbert_model = None
symptom_embeddings = None
if HAS_TRANSFORMERS and os.path.exists(EMBEDDINGS_PATH):
    try:
        sbert_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        symptom_embeddings = joblib.load(EMBEDDINGS_PATH)
    except Exception as e:
        print(f"Error loading SentenceTransformer or embeddings: {e}")

# Load ML model if available
rf_model = None
label_encoder = None
feature_columns = None
if HAS_ML_LIBS and not mock_data.USE_MOCK_MODEL:
    if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH) and os.path.exists(COLUMNS_PATH):
        try:
            rf_model = joblib.load(MODEL_PATH)
            label_encoder = joblib.load(ENCODER_PATH)
            with open(COLUMNS_PATH, "r") as f:
                feature_columns = json.load(f)
        except Exception as e:
            print(f"Error loading machine learning models: {e}")

DISCLAIMER = (
    "This tool is for triage support and informational purposes only. It is not a substitute for "
    "professional medical advice, diagnosis, or treatment. Always seek the advice of your physician "
    "or other qualified health provider with any questions you may have regarding a medical condition."
)

def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))

def string_match_symptoms(query: str, limit: int = 5) -> List[dict]:
    query_lower = query.lower().strip()
    matches = []
    for item in mock_data.MOCK_SYMPTOMS:
        name = item["canonical_name"].lower()
        if query_lower == name:
            score = 1.0
        elif name.startswith(query_lower):
            score = 0.8
        elif query_lower in name:
            score = 0.5
        else:
            score = 0.0
            
        if score > 0.0:
            matches.append((item, score))
            
    matches.sort(key=lambda x: x[1], reverse=True)
    return [item for item, score in matches[:limit]]

@app.get("/api/v1/symptoms", response_model=List[SymptomItem])
def get_symptoms(section: Optional[str] = None):
    """
    Return full list of symptoms, optionally filtered by section (head, chest, abdomen, limbs).
    """
    symptoms = mock_data.MOCK_SYMPTOMS
    if section:
        symptoms = [s for s in symptoms if s["section"].lower() == section.lower()]
    return symptoms

@app.get("/api/v1/symptoms/search", response_model=List[SymptomItem])
def search_symptoms(q: str = Query(..., min_length=1), limit: int = 5):
    """
    Search symptoms by query using semantic vector search or substring fallback.
    """
    # 1. Try vector similarity if embeddings/models are loaded
    if sbert_model and symptom_embeddings:
        try:
            query_emb = sbert_model.encode(q)
            results = []
            for item in mock_data.MOCK_SYMPTOMS:
                s_id = item["id"]
                name = item["canonical_name"]
                
                # Check mapping via id or name
                emb = symptom_embeddings.get(s_id) or symptom_embeddings.get(name)
                if emb is not None:
                    sim = cosine_similarity(query_emb, emb)
                    results.append((item, sim))
            
            if results:
                results.sort(key=lambda x: x[1], reverse=True)
                return [x[0] for x in results[:limit]]
        except Exception as e:
            print(f"Vector search failed, falling back to string match: {e}")
            
    # 2. Fallback to string matching
    return string_match_symptoms(q, limit)

@app.post("/api/v1/diagnose", response_model=DiagnosisResponse)
def diagnose(request: DiagnosisRequest):
    """
    Run diagnostic pipeline: model prediction / mock fallback, biological sex filtering, and logging.
    """
    status = "mock_fallback"
    predictions = []
    
    # 1. Attempt Machine Learning Model Diagnosis if present
    if rf_model and label_encoder and feature_columns and not mock_data.USE_MOCK_MODEL:
        try:
            # Compile feature vector
            vector = [0] * len(feature_columns)
            for input_symptom in request.symptoms:
                normalized = input_symptom.strip().lower()
                if normalized in feature_columns:
                    idx = feature_columns.index(normalized)
                    vector[idx] = 1
                    
            # Predict probabilities
            probs = rf_model.predict_proba([vector])[0]
            top_indices = np.argsort(probs)[::-1]
            
            for idx in top_indices:
                prob = float(probs[idx])
                if prob > 0.01:
                    disease_name = label_encoder.classes_[idx]
                    disease_key = disease_name.lower().replace(" ", "_")
                    disease_info = mock_data.MOCK_DISEASES.get(disease_key, {
                        "disease_id": disease_key,
                        "display_name": disease_name,
                        "urgency_level": "MEDIUM",
                        "description": f"Condition related to {disease_name}.",
                        "next_steps": ["Consult a medical professional for advice."],
                        "applicable_sex": None
                    })
                    
                    predictions.append({
                        "disease_id": disease_info["disease_id"],
                        "display_name": disease_info["display_name"],
                        "probability": round(prob, 3),
                        "urgency_level": disease_info["urgency_level"],
                        "description": disease_info["description"],
                        "next_steps": disease_info["next_steps"],
                        "applicable_sex": disease_info["applicable_sex"]
                    })
            status = "ml_prediction"
        except Exception as e:
            print(f"ML diagnosis failed, falling back to mock: {e}")
            predictions = []
            
    # 2. Mock Prediction Fallback
    if not predictions:
        status = "mock_fallback"
        predictions = mock_data.get_mock_predictions(request.symptoms)
        
    # 3. Biological Sex filtering
    patient_sex = request.metadata.sex
    filtered_preds = []
    for pred in predictions:
        applicable_sex = pred.get("applicable_sex")
        if patient_sex == "OTHER":
            filtered_preds.append(pred)
        elif applicable_sex is None:
            filtered_preds.append(pred)
        elif applicable_sex == patient_sex:
            filtered_preds.append(pred)
        else:
            # Contradicting biological sex constraint - drop prediction
            continue
            
    # Keep top 3 matched predictions
    final_predictions = filtered_preds[:3]
    
    # 4. Audit Log Write
    try:
        os.makedirs(DATA_LOGS_DIR, exist_ok=True)
        request_dict = request.model_dump() if hasattr(request, "model_dump") else request.dict()
        log_entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "request": request_dict,
            "status": status,
            "predictions": final_predictions
        }
        with open(AUDIT_LOG_PATH, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Failed writing audit log: {e}")
        
    # Build list of DiseasePrediction objects
    response_preds = [
        DiseasePrediction(
            disease_id=p["disease_id"],
            display_name=p["display_name"],
            probability=p["probability"],
            urgency_level=p["urgency_level"],
            description=p["description"],
            next_steps=p["next_steps"]
        ) for p in final_predictions
    ]
    
    return DiagnosisResponse(
        extracted_symptoms=request.symptoms,
        predictions=response_preds,
        status=status,
        disclaimer=DISCLAIMER
    )
