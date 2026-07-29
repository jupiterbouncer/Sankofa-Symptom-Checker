# Sankofa - Symptom Checker

> An AI-powered symptom checker that uses NLP vector embeddings and multi-class classification to suggest possible conditions based on user-reported symptoms.

## Course: CS 254 - Introduction to Artificial Intelligence | May–August 2026.

## Overview

Sankofa addresses a core limitation of lexical symptom matching — semantic gaps between how users describe symptoms and how they are labeled in medical datasets. By embedding symptoms into a vector space, the system can match "pain in the shoulder" to "shoulder pain" and return meaningful disease probability estimates.

---

## Setup

```bash
git clone https://github.com/your-team/sankofa-symptom-checker.git
cd sankofa-symptom-checker
pip install -r requirements.txt
```

---

## Installation

**Prerequisites:** Python 3.10+

Dataset: [drive.google.com/drive/folders/1g0x15qg93Gv1dsQj_GMuu-M1qKqqY3rs?usp=sharing](https://drive.google.com/drive/folders/1g0x15qg93Gv1dsQj_GMuu-M1qKqqY3rs?usp=sharing)

```powershell
# Clone the repo
git clone https://github.com/jupiterbouncer/Sankofa-Elenchus
cd sankofa-elenchus

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Running the App

```powershell
#line____________________
```

Then open `http://localhost:____` in your browser.

---

## Project Structure

| Folder       | Purpose                                               |
| ------------ | ----------------------------------------------------- |
| `data/`      | Raw, processed datasets and embeddings                |
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

- HuggingFace symptom-disease datasets
- Augmented symptom severity data

---

_This project was built as part of CS 254 - Introduction to AI at Ashesi University._
