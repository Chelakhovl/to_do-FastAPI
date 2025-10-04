from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib


def load_dataset(csv_path: Path) -> Tuple[List[str], List[str]]:
    X, y = [], []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = (row.get("task_description") or "").strip()
            prio = (row.get("priority") or "").strip().lower()
            if not desc or prio not in {"high", "low"}:
                continue
            X.append(desc)
            y.append(prio)
    if not X:
        raise ValueError("Dataset is empty or invalid.")
    return X, y


def train(csv_path: Path, out_path: Path, do_eval: bool = False) -> Path:
    X, y = load_dataset(csv_path)

    pipe: Pipeline = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", LogisticRegression(max_iter=500, class_weight="balanced")),
        ]
    )

    if do_eval and len(X) >= 4:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, stratify=y, random_state=42
        )
        pipe.fit(X_train, y_train)
        
        print(classification_report(y_test, pipe.predict(X_test), zero_division=0))
    else:
       
        pipe.fit(X, y)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, out_path)
    return out_path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train text classifier for task priority (high/low).")
    p.add_argument("--csv", required=True, help="Path to CSV with columns: task_description,priority")
    p.add_argument("--out", default="models/task_priority_model.joblib", help="Output model path")
    p.add_argument("--eval", action="store_true", help="Run a tiny holdout evaluation (optional)")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    model_path = train(Path(args.csv), Path(args.out), do_eval=args.eval)
    print(f"Model saved to: {Path(model_path).resolve()}")
