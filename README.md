# Sankofa - Symptom Checker

> An AI-powered symptom checker that uses NLP vector embeddings and multi-class classification to suggest possible conditions based on user-reported symptoms.

## Course: CS 254 - Introduction to Artificial Intelligence | May-August 2026.

## Project Overview

Sankofa addresses a core limitation of lexical symptom matching: semantic gaps between how users describe symptoms and how they are labeled in medical datasets. By embedding symptoms into a vector space, the system can match descriptions like "pain in the shoulder" to a known symptom such as "shoulder pain" and return disease probability estimates.

The project includes a trained machine learning model, symptom feature mappings, notebooks for the AI pipeline, and early frontend/API folders for the symptom-checking interface.

---

## Setup and Installation

**Prerequisites:** Python 3.10+ and `pip`

Dataset: [drive.google.com/drive/folders/1g0x15qg93Gv1dsQj_GMuu-M1qKqqY3rs?usp=sharing](https://drive.google.com/drive/folders/1g0x15qg93Gv1dsQj_GMuu-M1qKqqY3rs?usp=sharing)

```powershell
# Clone the repo
git clone https://github.com/jupiterbouncer/Sankofa-Elenchus
cd Sankofa-Elenchus

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies from requirements.txt
pip install -r requirements.txt
```

---

## Running the App

The final app run command will be added once the API/frontend startup flow is confirmed.

```powershell
# Run command coming later
```

---

## Usage Example

The prediction module can be used directly with a list of symptom names:

```python
from src.models.predict import predict

symptoms = [
    "joint pain",
    "joint swelling",
    "muscle pain",
    "muscle weakness",
]

predictions = predict(symptoms, top_n=5)

for result in predictions:
    print(f"{result['disease']}: {result['probability']}%")
```

---

## Project Structure

| Folder         | Purpose                                               |
| -------------- | ----------------------------------------------------- |
| `data/`      | Raw, processed datasets and embeddings                |
| `model/`     | Trained model and supporting encoder/feature files    |
| `notebooks/` | EDA through evaluation, numbered by ML pipeline stage |
| `src/`       | Core ML pipeline - embeddings, classifier, API        |
| `frontend/`  | UI - body map, symptom search, results                |
| `ethics/`    | Bias, fairness, and privacy audit                     |

---

## Team

| Name                 | Role                             |
| -------------------- | -------------------------------- |
| Karen Kwatia         | QA Engineer & Documentation Lead |
| Emmanuel Nkunim      | Prompt Engineer & Presenter      |
| Daniel Eta           | ML & Software Engineer           |
| Oluwademilade Subair | QA Engineer & UI/UX              |

---

## Dataset Sources

- Kaggle symptom-disease datasets
- Augmented symptom severity data
