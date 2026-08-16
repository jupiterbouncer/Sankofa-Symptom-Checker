# %% [markdown]
# ## Import & loading

# %%
import joblib
import numpy as np
import pandas as pd

# Load model and encoder
rf = joblib.load("model/random_forest.pkl")
le = joblib.load("model/label_encoder.pkl")
SYMPTOM_COLUMNS = joblib.load("model/symptom_columns.pkl")

# %% [markdown]
# ## Retrieving exact same columns used to learn

# %% [markdown]
# ## PREDICT FUNCTION (CUSTOMIZABLE TO RETURN TOP N prediction)

# %%
def predict(symptoms: list[str], top_n: int = 5) -> list[dict]:
    """
    Takes a list of symptoms and returns top n disease predictions
    """

    input_vector = np.zeros(len(SYMPTOM_COLUMNS))

    for symptom in symptoms:
        symptom = symptom.strip().lower()

        if symptom in SYMPTOM_COLUMNS:
            idx = SYMPTOM_COLUMNS.index(symptom)
            input_vector[idx] = 1
        else:
            print(f"Warning: unknown symptom '{symptom}'")

    input_df = pd.DataFrame([input_vector], columns=SYMPTOM_COLUMNS)

    # Get probabilities
    probabilities = rf.predict_proba(input_df)[0]

    # Get top n predictions
    top_indices = np.argsort(probabilities)[::-1][:top_n]

    results = []
    for idx in top_indices:
        encoded_classes = rf.classes_[idx]
        disease = le.inverse_transform([encoded_classes])[0]

        results.append(
            {
                "disease": disease,
                "probability": round(float(probabilities[idx]) * 100, 2),
            }
        )

    return results

# %% [markdown]
# The function handles the full inference process. It starts by creating a binary input vector with one position for every symptom in `SYMPTOM_COLUMNS`. For each symptom provided, it cleans the text, checks whether the symptom is recognized, and sets the corresponding position to 1. Unknown symptoms are ignored with a warning.
# 
# The vector is then converted into a DataFrame using the same feature names and order the Random Forest was trained on. `predict_proba()` returns the model’s probability distribution across all disease classes. The probabilities are sorted from highest to lowest, the top n classes are decoded back into disease names using the label encoder, and the function returns the disease names with their percentage scores.

# %% [markdown]
# ## MAIN

# %%
if __name__ == "__main__":
  SYMPTOM_GROUPS = {
    "respiratory": [
        "cough",
        "shortness of breath",
        "wheezing",
        "chest tightness",
        "coughing up sputum",
        "fever",
    ],

    "musculoskeletal": [
        "joint pain",
        "joint swelling",
        "muscle pain",
        "muscle weakness",
        "joint stiffness or tightness",
        "cramps and spasms",
    ],

    "neurological": [
        "headache",
        "dizziness",
        "loss of sensation",
        "focal weakness",
        "slurring words",
        "disturbance of memory",
    ],

    "gastrointestinal": [
        "nausea",
        "vomiting",
        "diarrhea",
        "sharp abdominal pain",
        "upper abdominal pain",
        "stomach bloating",
    ],

    "urinary": [
        "painful urination",
        "frequent urination",
        "blood in urine",
        "lower abdominal pain",
        "unusual color or odor to urine",
        "fever",
    ],

    "cardiac": [
        "sharp chest pain",
        "chest tightness",
        "palpitations",
        "irregular heartbeat",
        "shortness of breath",
        "dizziness",
    ],

    "skin": [
        "skin rash",
        "itching of skin",
        "skin irritation",
        "skin swelling",
        "skin pain",
        "abnormal appearing skin",
    ],

    "mental_health": [
        "anxiety and nervousness",
        "depression",
        "insomnia",
        "low self-esteem",
        "fears and phobias",
        "obsessions and compulsions",
    ],

    "eye": [
        "pain in eye",
        "eye redness",
        "diminished vision",
        "double vision",
        "itchiness of eye",
        "lacrimation",
    ],

    "ent": [                  # eyes, nose and throat
        "sore throat",
        "nasal congestion",
        "ear pain",
        "diminished hearing",
        "sinus congestion",
        "painful sinuses",
    ],
}

  # Just to confirm symptoms are actually in the csv and recognised
  for category, symptoms in SYMPTOM_GROUPS.items():
    valid = [s for s in symptoms if s in SYMPTOM_COLUMNS]
    invalid = [s for s in symptoms if s not in SYMPTOM_COLUMNS]

    print(f"\n{category.upper()}")
    print("Valid:", valid)
    print("Invalid:", invalid)

    predictions = predict(symptoms)
    for p in predictions:
      print(f"{p['disease']}: {p['probability']}%")

# %% [markdown]
# The `main` section is just a testing and validation setup. `SYMPTOM_GROUPS` contains realistic groups of symptoms from different body systems, such as respiratory, neurological, urinary, and cardiac symptoms.
# 
# For each category, the code first checks that every symptom actually exists in `SYMPTOM_COLUMNS`. It prints which symptoms are valid or invalid, then passes the group into `predict()` and displays the model’s top five disease predictions.
