from typing import List, Dict, Any, Optional

# Flag to enable/disable mock fallback
USE_MOCK_MODEL = True

MOCK_SYMPTOMS = [
    # Head section
    {"id": "s1", "canonical_name": "headache", "section": "head", "applicable_sex": None},
    {"id": "s2", "canonical_name": "dizziness", "section": "head", "applicable_sex": None},
    {"id": "s3", "canonical_name": "anxiety and nervousness", "section": "head", "applicable_sex": None},
    {"id": "s4", "canonical_name": "insomnia", "section": "head", "applicable_sex": None},
    {"id": "s5", "canonical_name": "depression", "section": "head", "applicable_sex": None},
    {"id": "s6", "canonical_name": "sore throat", "section": "head", "applicable_sex": None},
    {"id": "s7", "canonical_name": "runny nose", "section": "head", "applicable_sex": None},
    
    # Chest section
    {"id": "s8", "canonical_name": "shortness of breath", "section": "chest", "applicable_sex": None},
    {"id": "s9", "canonical_name": "sharp chest pain", "section": "chest", "applicable_sex": None},
    {"id": "s10", "canonical_name": "chest tightness", "section": "chest", "applicable_sex": None},
    {"id": "s11", "canonical_name": "cough", "section": "chest", "applicable_sex": None},
    {"id": "s12", "canonical_name": "heart palpitations", "section": "chest", "applicable_sex": None},
    
    # Abdomen section
    {"id": "s13", "canonical_name": "nausea", "section": "abdomen", "applicable_sex": None},
    {"id": "s14", "canonical_name": "abdominal pain", "section": "abdomen", "applicable_sex": None},
    {"id": "s15", "canonical_name": "heartburn", "section": "abdomen", "applicable_sex": None},
    {"id": "s16", "canonical_name": "vomiting", "section": "abdomen", "applicable_sex": None},
    {"id": "s17", "canonical_name": "diarrhea", "section": "abdomen", "applicable_sex": None},
    {"id": "s18", "canonical_name": "ovarian pain", "section": "abdomen", "applicable_sex": "F"},
    {"id": "s19", "canonical_name": "prostate pain", "section": "abdomen", "applicable_sex": "M"},
    
    # Limbs section
    {"id": "s20", "canonical_name": "joint pain", "section": "limbs", "applicable_sex": None},
    {"id": "s21", "canonical_name": "muscle weakness", "section": "limbs", "applicable_sex": None},
    {"id": "s22", "canonical_name": "leg swelling", "section": "limbs", "applicable_sex": None},
    {"id": "s23", "canonical_name": "ankle weakness", "section": "limbs", "applicable_sex": None},
    {"id": "s24", "canonical_name": "hip weakness", "section": "limbs", "applicable_sex": None},
]

MOCK_DISEASES = {
    "panic_disorder": {
        "disease_id": "panic_disorder",
        "display_name": "Panic Disorder",
        "urgency_level": "LOW",
        "description": "An anxiety disorder characterized by recurrent unexpected panic attacks.",
        "next_steps": [
            "Practice deep breathing exercises",
            "Consult a mental health professional",
            "Reduce caffeine and stimulant intake"
        ],
        "applicable_sex": None,
        "associated_symptoms": ["anxiety and nervousness", "depression", "shortness of breath", "chest tightness", "heart palpitations"]
    },
    "angina": {
        "disease_id": "angina",
        "display_name": "Angina Pectoris",
        "urgency_level": "HIGH",
        "description": "Chest pain or discomfort caused when your heart muscle doesn't get enough oxygen-rich blood.",
        "next_steps": [
            "Rest immediately if chest pain occurs",
            "Seek emergency medical attention if pain worsens or persists",
            "Consult a cardiologist"
        ],
        "applicable_sex": None,
        "associated_symptoms": ["sharp chest pain", "chest tightness", "shortness of breath", "heart palpitations"]
    },
    "common_cold": {
        "disease_id": "common_cold",
        "display_name": "Common Cold",
        "urgency_level": "LOW",
        "description": "A viral infection of your nose and throat (upper respiratory tract).",
        "next_steps": [
            "Stay hydrated and get plenty of rest",
            "Use over-the-counter pain relievers or decongestants",
            "Monitor temperature and seek help if high fever develops"
        ],
        "applicable_sex": None,
        "associated_symptoms": ["sore throat", "runny nose", "cough", "headache"]
    },
    "gastroenteritis": {
        "disease_id": "gastroenteritis",
        "display_name": "Gastroenteritis",
        "urgency_level": "MEDIUM",
        "description": "An intestinal infection marked by watery diarrhea, abdominal cramps, nausea or vomiting, and sometimes fever.",
        "next_steps": [
            "Drink plenty of fluids with electrolytes to prevent dehydration",
            "Eat bland foods when ready",
            "Avoid dairy, caffeine, and alcohol"
        ],
        "applicable_sex": None,
        "associated_symptoms": ["nausea", "abdominal pain", "vomiting", "diarrhea"]
    },
    "ovarian_cyst": {
        "disease_id": "ovarian_cyst",
        "display_name": "Ovarian Cyst",
        "urgency_level": "MEDIUM",
        "description": "Fluid-filled sacs in an ovary or on its surface, which are common and pelvic-pain-inducing but usually harmless.",
        "next_steps": [
            "Consult a gynecologist for evaluation",
            "Monitor pelvic pain severity",
            "Use warm compresses for mild pelvic discomfort"
        ],
        "applicable_sex": "F",
        "associated_symptoms": ["ovarian pain", "abdominal pain", "nausea"]
    },
    "prostatitis": {
        "disease_id": "prostatitis",
        "display_name": "Prostatitis",
        "urgency_level": "MEDIUM",
        "description": "Inflammation or infection of the prostate gland, causing pelvic pain and urinary discomfort.",
        "next_steps": [
            "Consult a urologist for diagnosis",
            "Drink plenty of water to help flush the urinary tract",
            "Avoid alcohol, caffeine, and spicy foods"
        ],
        "applicable_sex": "M",
        "associated_symptoms": ["prostate pain", "abdominal pain", "joint pain"]
    }
}

def get_mock_predictions(input_symptoms: List[str]) -> List[Dict[str, Any]]:
    predictions = []
    # Normalize input symptoms
    normalized_inputs = [s.strip().lower() for s in input_symptoms]
    
    for key, disease in MOCK_DISEASES.items():
        associated = disease["associated_symptoms"]
        # Find overlap
        overlap = set(normalized_inputs).intersection(set(associated))
        if overlap:
            # Score proportional to the overlap size
            score = len(overlap) / len(associated)
            # Ensure probability lies between 0.15 and 0.95
            probability = round(0.15 + 0.80 * score, 3)
            predictions.append({
                "disease_id": disease["disease_id"],
                "display_name": disease["display_name"],
                "probability": probability,
                "urgency_level": disease["urgency_level"],
                "description": disease["description"],
                "next_steps": disease["next_steps"],
                "applicable_sex": disease["applicable_sex"]
            })
            
    # Sort predictions by probability descending
    predictions.sort(key=lambda x: x["probability"], reverse=True)
    return predictions
