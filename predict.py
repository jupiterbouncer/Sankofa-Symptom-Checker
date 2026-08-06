{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "gpuType": "T4",
      "authorship_tag": "ABX9TyOElwm5FUZqES/QiKvzZHzc",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    },
    "accelerator": "GPU"
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/jupiterbouncer/Sankofa-Symptom-Checker/blob/feature%2Finference-pipeline/predict.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Import & loading"
      ],
      "metadata": {
        "id": "jBIUjA2ugcu8"
      }
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "d02eXtS9YmcR"
      },
      "outputs": [],
      "source": [
        "import joblib\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "from google.colab import drive\n",
        "\n",
        "drive.mount(\"/content/drive\")\n",
        "\n",
        "# Load model and encoder\n",
        "rf = joblib.load(\"/content/drive/MyDrive/SE-dataset/random_forest.pkl\")\n",
        "le = joblib.load(\"/content/drive/MyDrive/SE-dataset/label_encoder.pkl\")"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Retrieving exact same columns used to learn"
      ],
      "metadata": {
        "id": "8EN3O8BzgYBM"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "SYMPTOM_COLUMNS = (\n",
        "    pd.read_csv(\"/content/drive/MyDrive/SE-dataset/cleaned_diseases_symptoms.csv\")\n",
        "    .drop(columns=[\"diseases\"])\n",
        "    .columns\n",
        "    .tolist()\n",
        ")"
      ],
      "metadata": {
        "id": "5jR4D-Orf-n2"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "## PREDICT FUNCTION (CUSTOMIZABLE TO RETURN TOP N prediction)"
      ],
      "metadata": {
        "id": "FgnFEwrmgRkS"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "def predict(symptoms: list[str], top_n: int = 5) -> list[dict]:\n",
        "    \"\"\"\n",
        "    Takes a list of symptoms and returns top n disease predictions\n",
        "    \"\"\"\n",
        "\n",
        "    input_vector = np.zeros(len(SYMPTOM_COLUMNS))\n",
        "\n",
        "    for symptom in symptoms:\n",
        "        symptom = symptom.strip().lower()\n",
        "\n",
        "        if symptom in SYMPTOM_COLUMNS:\n",
        "            idx = SYMPTOM_COLUMNS.index(symptom)\n",
        "            input_vector[idx] = 1\n",
        "        else:\n",
        "            print(f\"Warning: unknown symptom '{symptom}'\")\n",
        "\n",
        "    input_df = pd.DataFrame([input_vector], columns=SYMPTOM_COLUMNS)\n",
        "\n",
        "    # Get probabilities\n",
        "    probabilities = rf.predict_proba(input_df)[0]\n",
        "\n",
        "    # Get top n predictions\n",
        "    top_indices = np.argsort(probabilities)[::-1][:top_n]\n",
        "\n",
        "    results = []\n",
        "    for idx in top_indices:\n",
        "        encoded_classes = rf.classes_[idx]\n",
        "        disease = le.inverse_transform([encoded_classes])[0]\n",
        "\n",
        "        results.append(\n",
        "            {\n",
        "                \"disease\": disease,\n",
        "                \"probability\": round(float(probabilities[idx]) * 100, 2),\n",
        "            }\n",
        "        )\n",
        "\n",
        "    return results"
      ],
      "metadata": {
        "id": "5YhIq1ExgHw8"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "## MAIN"
      ],
      "metadata": {
        "id": "EBg0mGhogKvu"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "if __name__ == \"__main__\":\n",
        "  musculoskeletal = [\n",
        "    \"joint pain\",\n",
        "    \"joint swelling\",\n",
        "    \"muscle pain\",\n",
        "    \"muscle weakness\",\n",
        "    \"joint stiffness or tightness\",\n",
        "    \"cramps and spasms\"\n",
        "    ]\n",
        "\n",
        "  # Just to confirm symptoms are actually in the csv and recognised\n",
        "  valid_symptoms = [s for s in musculoskeletal if s in SYMPTOM_COLUMNS]\n",
        "  invalid_symptoms = [s for s in musculoskeletal if s not in SYMPTOM_COLUMNS]\n",
        "\n",
        "  print(\"Valid:\", valid_symptoms)\n",
        "  print(\"Invalid:\", invalid_symptoms)\n",
        "\n",
        "  predictions = predict(musculoskeletal)\n",
        "  for p in predictions:\n",
        "      print(f\"{p['disease']}: {p['probability']}%\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "1cILCd7japU4",
        "outputId": "8bfd8910-6767-4a86-8f1c-60f04f53c84c"
      },
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Valid: ['joint pain', 'joint swelling', 'muscle pain', 'muscle weakness', 'joint stiffness or tightness', 'cramps and spasms']\n",
            "Invalid: []\n",
            "adhesive capsulitis of the shoulder: 13.06%\n",
            "rheumatoid arthritis: 12.55%\n",
            "plantar fasciitis: 11.44%\n",
            "osteoarthritis: 9.91%\n",
            "epilepsy: 9.01%\n"
          ]
        }
      ]
    }
  ]
}