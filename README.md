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

To run the application, you will need to start both the FastAPI backend server and the Vue/Vite frontend dev server.

### 1. Starting the FastAPI Backend API

The backend handles semantic symptom search and disease diagnosis:

```bash
# Ensure your virtual environment is active
# Linux/macOS:
source venv/bin/activate
# Windows:
.\venv\Scripts\Activate.ps1

# Run the Uvicorn server on port 8000
uvicorn src.api.app:app --reload --port 8000
```

The interactive API documentation will be available at `http://localhost:8000/docs` (Swagger UI).

### 2. Starting the Frontend Dev Server

The frontend provides an interactive body map and diagnostic results sidepane:

```bash
# Navigate to the frontend directory
cd frontend

# Install Node dependencies (if running for the first time)
npm install

# Run the Vite dev server
npm run dev
```

Once running, open your browser to the local development URL (typically `http://localhost:5173`).

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
