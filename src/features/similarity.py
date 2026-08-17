from pathlib import Path
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

# Resolve project root dynamically (two levels up from src/features/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EMBEDDINGS_PATH = (
    PROJECT_ROOT / "data" / "embeddings" / "symptom_vectors.joblib"
)


class SemanticSymptomSearch:
    def __init__(self, artifact_path: Path | str = DEFAULT_EMBEDDINGS_PATH):
        path = Path(artifact_path)
        if not path.exists():
            raise FileNotFoundError(f"Embedding artifact not found at {path.resolve()}")

        data = joblib.load(path)
        self.symptom_features = data["symptom_features"]
        self.canonical_names = data.get("canonical_names", self.symptom_features)
        self.embeddings = data["embeddings"]
        self.default_threshold = data.get("threshold", 0.38)

        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def search(self, query: str, top_k: int = 5, min_score: float = None) -> list[dict]:
        if not query.strip():
            return []

        threshold = min_score if min_score is not None else self.default_threshold
        query_vec = self.model.encode([query], normalize_embeddings=True)

        scores = np.dot(query_vec, self.embeddings.T)[0]
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(scores[idx])
            if score >= threshold:
                results.append(
                    {
                        "feature_id": self.symptom_features[idx],
                        "display_name": self.canonical_names[idx],
                        "similarity_score": round(score, 4),
                    }
                )
        return results
