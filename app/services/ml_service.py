from __future__ import annotations

import os
from pathlib import Path
from typing import Tuple

import joblib


class MLService:
    """Lightweight wrapper around a scikit-learn pipeline saved via joblib."""

    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = Path(model_path or os.getenv("MODEL_PATH", "models/task_priority_model.joblib"))
        self._model = None  # lazy-loaded

    def _ensure_loaded(self) -> None:
        if self._model is None:
            if not self.model_path.exists():
                raise FileNotFoundError(f"Model not found at: {self.model_path}")
            self._model = joblib.load(self.model_path)

    def predict(self, text: str) -> Tuple[str, float]:
        """Return (label, confidence) for given text."""
        self._ensure_loaded()
        proba = self._model.predict_proba([text])[0]
        classes = list(self._model.classes_)  # ['high','low'] (order by training)
        idx = int(proba.argmax())
        label = str(classes[idx])
        confidence = float(proba[idx])
        return label, confidence


# Shared instance
ml_service = MLService()
