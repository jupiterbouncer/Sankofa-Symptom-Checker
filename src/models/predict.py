from pathlib import Path

import joblib
import numpy as np

# Resolve project root dynamically (two levels up from src/models/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "model" / "random_forest.pkl"
# Use the line below if you do not have the larger random_forest.pkl file locally
# DEFAULT_MODEL_PATH = PROJECT_ROOT / "model" / "classifier.joblib"
DEFAULT_ENCODER_PATH = PROJECT_ROOT / "model" / "label_encoder.pkl"
DEFAULT_FEATURES_PATH = PROJECT_ROOT / "data" / "embeddings" / "symptom_vectors.joblib"

class DiseasePredictor:
    def __init__(
        self,
        model_path: Path | str = DEFAULT_MODEL_PATH,
        label_encoder_path: Path | str = DEFAULT_ENCODER_PATH,
        features_path: Path | str = DEFAULT_FEATURES_PATH,
    ):
        model_p = Path(model_path)
        encoder_p = Path(label_encoder_path)
        feat_p = Path(features_path)

        if not feat_p.exists():
            raise FileNotFoundError(
                f"Feature vector artifact not found at {feat_p.resolve()}"
            )

        feat_data = joblib.load(feat_p)
        self.feature_columns = feat_data["symptom_features"]
        self.feature_index_map = {
            feat: i for i, feat in enumerate(self.feature_columns)
        }

        self.model = joblib.load(model_p) if model_p.exists() else None
        self.label_encoder = joblib.load(encoder_p) if encoder_p.exists() else None

    def vectorize_symptoms(self, active_symptoms: list[str]) -> np.ndarray:
        vector = np.zeros((1, len(self.feature_columns)), dtype=np.uint8)
        for sym in active_symptoms:
            clean_sym = sym.strip().lower()
            if clean_sym in self.feature_index_map:
                vector[0, self.feature_index_map[clean_sym]] = 1
        return vector

    def predict(self, active_symptoms: list[str], top_k: int = 3) -> list[dict]:
        if self.model is None or self.label_encoder is None:
            raise RuntimeError("Classifier or label encoder artifact missing.")

        X_input = self.vectorize_symptoms(active_symptoms)

        if np.sum(X_input) == 0:
            return []

        probabilities = self.model.predict_proba(X_input)[0]
        top_indices = np.argsort(probabilities)[::-1][:top_k]

        predictions = []
        for idx in top_indices:
            disease_name = self.label_encoder.inverse_transform([idx])[0]
            prob = float(probabilities[idx])
            if prob > 0.01:
                predictions.append(
                    {
                        "disease": disease_name,
                        "probability": round(prob, 4),
                    }
                )

        return predictions
