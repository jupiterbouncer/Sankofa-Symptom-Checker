from pydantic import BaseModel
from typing import List, Optional, Literal

class PatientMetadata(BaseModel):
    age: Optional[int] = None
    sex: Literal['M', 'F', 'OTHER']
    bmi: Optional[float] = None

class DiagnosisRequest(BaseModel):
    symptoms: List[str]
    metadata: PatientMetadata

class DiseasePrediction(BaseModel):
    disease_id: str
    display_name: str
    probability: float
    urgency_level: str
    description: str
    next_steps: List[str]

class DiagnosisResponse(BaseModel):
    extracted_symptoms: List[str]
    predictions: List[DiseasePrediction]
    status: str
    disclaimer: str

class SymptomItem(BaseModel):
    id: str
    canonical_name: str
    section: str
    applicable_sex: Optional[Literal['M', 'F']] = None
