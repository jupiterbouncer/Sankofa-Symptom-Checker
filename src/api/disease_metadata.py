def get_disease_metadata(disease_name: str, probability: float) -> dict:
    name_lower = disease_name.lower()
    
    # List of keywords for high-acuity/serious conditions
    serious_keywords = [
        "heart attack", "cardiac arrest", "aneurysm", "stroke", "sepsis", 
        "peritonitis", "meningitis", "embolism", "hemorrhage", "pneumothorax", 
        "ketoacidosis", "failure", "respiratory distress", "cancer", "poisoning", 
        "appendicitis", "pancreatitis", "fracture", "occlusion"
    ]
    
    is_serious = any(kw in name_lower for kw in serious_keywords) or probability > 0.70
    urgency = "Urgent" if is_serious else "Routine"
    
    # Titlecase disease name for display
    display_title = disease_name.title()
    
    # Tailored summaries and treatment plans based on categories
    if is_serious:
        summary = (
            f"{display_title} is a high-severity clinical condition. "
            f"It typically presents as a critical systemic or organ-specific crisis "
            f"that requires rapid diagnostic assessment (such as imaging, lab panels) "
            f"to prevent severe, long-term physiological complications or life-threatening progression."
        )
        treatment = (
            f"IMMEDIATE CLINICAL EVALUATION IS REQUIRED. Please seek emergency medical care, "
            f"visit the nearest emergency department, or contact emergency services immediately. "
            f"Hospital-based intervention, monitoring, and stabilization are necessary."
        )
    elif any(kw in name_lower for kw in ["chronic", "arthritis", "diabetes", "copd", "gerd", "syndrome", "disease", "anemia"]):
        summary = (
            f"{display_title} is a chronic or progressive condition. "
            f"It involves ongoing physiological changes that require long-term management, "
            f"lifestyle modifications, and routine monitoring to control symptoms and maintain quality of life."
        )
        treatment = (
            f"Management plans typically focus on symptom control and preventing disease progression. "
            f"This includes prescribed maintenance medications, targeted physical therapy, "
            f"dietary modifications, and regular follow-up consultations with your primary care provider."
        )
    elif any(kw in name_lower for kw in ["acute", "infection", "bronchitis", "sinusitis", "cold", "flu", "allergy", "dermatitis"]):
        summary = (
            f"{display_title} is an acute inflammatory or infectious response. "
            f"It is usually temporary and self-limiting in nature, but can cause noticeable discomfort "
            f"and localized symptoms."
        )
        treatment = (
            f"Recommended actions include supportive care (adequate rest, hydration), "
            f"over-the-counter symptomatic relief (antihistamines, decongestants, or pain relievers), "
            f"and consulting a doctor if symptoms persist beyond a few days or worsen."
        )
    else:
        summary = (
            f"A clinical evaluation is recommended to investigate the possibility of {display_title}. "
            f"This profile is based on reported symptom matches and requires diagnostic verification "
            f"by a medical professional."
        )
        treatment = (
            f"Please schedule a consultation with a healthcare provider for a thorough examination. "
            f"They will discuss your medical history, perform necessary diagnostic tests, and formulate "
            f"a customized management plan."
        )
        
    return {
        "urgency": urgency,
        "serious": is_serious,
        "summary": summary,
        "treatment": treatment
    }
