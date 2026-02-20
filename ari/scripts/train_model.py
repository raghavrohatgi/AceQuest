#!/usr/bin/env python3
"""
Phase 3 — ARI Model Training
Trains Ridge regression and Gradient Boosting models on the feature matrix,
evaluates both, picks the winner by MAE, calibrates, and serialises to .pkl.

Input:  /ari/data/corpus-features.csv
Output: /ari/models/ari-model-v1.pkl
        /ari/models/model-card.json

Success gate: MAE ≤ 0.8 on held-out test set.

Run: python3 ari/scripts/train_model.py
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DATA_DIR = Path("/Users/raghavrohatgi/Documents/AceQuest/ari/data")
MODELS_DIR = Path("/Users/raghavrohatgi/Documents/AceQuest/ari/models")
INPUT_FILE = DATA_DIR / "corpus-features.csv"
MODEL_FILE = MODELS_DIR / "ari-model-v1.pkl"
CARD_FILE = MODELS_DIR / "model-card.json"

FEATURE_COLS = [
    "mean_word_frequency_rank",
    "mean_sentence_length",
    "type_token_ratio",
    "avg_syllables_per_word",
    "pct_rare_words",
    "mean_log_freq_rank",
    "lexical_density",
    "flesch_kincaid_grade",
    "gunning_fog",
    "sentence_length_variance",
    "subordinate_clause_ratio",
    "long_word_ratio",
]

MAE_GATE = 0.8   # success threshold


def load_data() -> tuple[pd.DataFrame, pd.Series]:
    """Load and validate the feature CSV."""
    print(f"Loading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    print(f"  Rows: {len(df):,} | Grades: {sorted(df['grade'].unique())}")

    # Drop any rows with missing features
    before = len(df)
    df = df.dropna(subset=FEATURE_COLS + ["grade"])
    if len(df) < before:
        print(f"  Dropped {before - len(df)} rows with missing values")

    X = df[FEATURE_COLS]
    y = df["grade"].astype(float)
    return X, y, df


def train_and_evaluate(X_train, X_test, y_train, y_test):
    """Train Ridge and GBR models, return results dict for each."""
    models = {
        "Ridge": Pipeline([
            ("scaler", StandardScaler()),
            ("model", Ridge(alpha=1.0)),
        ]),
        "GradientBoosting": Pipeline([
            ("scaler", StandardScaler()),
            ("model", GradientBoostingRegressor(
                n_estimators=200,
                max_depth=4,
                learning_rate=0.05,
                subsample=0.8,
            )),
        ]),
    }

    results = {}
    for name, pipeline in models.items():
        print(f"\n  Training {name}...")
        pipeline.fit(X_train, y_train)

        # 5-fold CV on training set
        cv_scores = cross_val_score(
            pipeline, X_train, y_train,
            cv=5, scoring="neg_mean_absolute_error"
        )
        cv_mae = -cv_scores.mean()

        # Test set evaluation
        y_pred = pipeline.predict(X_test)
        # Clamp predictions to 1–10 range
        y_pred_clamped = np.clip(y_pred, 1.0, 10.0)
        test_mae = mean_absolute_error(y_test, y_pred_clamped)
        test_r2 = r2_score(y_test, y_pred_clamped)

        # Per-grade MAE breakdown
        test_df = pd.DataFrame({"grade": y_test, "pred": y_pred_clamped})
        per_grade_mae = test_df.groupby("grade").apply(
            lambda g: mean_absolute_error(g["grade"], g["pred"])
        ).to_dict()

        results[name] = {
            "pipeline": pipeline,
            "cv_mae": cv_mae,
            "test_mae": test_mae,
            "test_r2": test_r2,
            "per_grade_mae": {int(k): round(v, 3) for k, v in per_grade_mae.items()},
        }
        print(f"    CV MAE  : {cv_mae:.3f}")
        print(f"    Test MAE: {test_mae:.3f}")
        print(f"    Test R²  : {test_r2:.3f}")

    return results


def print_per_grade_breakdown(results: dict, winner: str) -> None:
    print(f"\n  Per-grade MAE ({winner}):")
    print(f"  {'Grade':>6}  {'MAE':>6}  {'Status':>8}")
    print(f"  {'-'*25}")
    for grade, mae in sorted(results[winner]["per_grade_mae"].items()):
        status = "✓" if mae <= 1.0 else "⚠"
        print(f"  {grade:>6}  {mae:>6.3f}  {status}")


def within_one_grade_accuracy(pipeline, X_test, y_test) -> float:
    """% of predictions within ±1 grade of true grade."""
    y_pred = np.clip(pipeline.predict(X_test), 1.0, 10.0)
    within_one = np.abs(y_pred - y_test.values) <= 1.0
    return within_one.mean() * 100


def main():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    X, y, df = load_data()

    # Stratified train/test split (80/20) by grade
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y
    )
    print(f"\nTrain: {len(X_train):,} | Test: {len(X_test):,}")

    print("\n=== TRAINING MODELS ===")
    results = train_and_evaluate(X_train, X_test, y_train, y_test)

    # Pick winner by test MAE
    winner = min(results, key=lambda k: results[k]["test_mae"])
    loser = [k for k in results if k != winner][0]
    print(f"\n=== WINNER: {winner} ===")
    print(f"  (MAE {results[winner]['test_mae']:.3f} vs {results[loser]['test_mae']:.3f} for {loser})")

    print_per_grade_breakdown(results, winner)

    winning_pipeline = results[winner]["pipeline"]
    test_mae = results[winner]["test_mae"]
    test_r2 = results[winner]["test_r2"]

    # Within-1-grade accuracy
    acc = within_one_grade_accuracy(winning_pipeline, X_test, y_test)
    print(f"\n  Within ±1 grade accuracy: {acc:.1f}%")

    # MAE gate check
    print(f"\n=== MAE GATE: ≤ {MAE_GATE} ===")
    if test_mae <= MAE_GATE:
        print(f"  ✓ PASSED — MAE {test_mae:.3f}")
    else:
        print(f"  ✗ FAILED — MAE {test_mae:.3f} > {MAE_GATE}")
        print("  Diagnosis: Check corpus coverage per grade (run corpus_builder.py --stats)")
        print("  Do NOT reach for a more complex model — fix the data first.")

    # Feature importance (GBR only)
    if winner == "GradientBoosting":
        model = winning_pipeline.named_steps["model"]
        importances = dict(zip(FEATURE_COLS, model.feature_importances_))
        print(f"\n  Feature importances:")
        for feat, imp in sorted(importances.items(), key=lambda x: -x[1]):
            bar = "█" * int(imp * 40)
            print(f"    {feat:<30} {imp:.3f}  {bar}")

    # Serialise model
    joblib.dump(winning_pipeline, MODEL_FILE)
    print(f"\n  Model saved: {MODEL_FILE}")

    # Write model card
    card = {
        "model_name": "ari-model-v1",
        "model_type": winner,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "corpus_size": len(X),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "features": FEATURE_COLS,
        "target": "CBSE grade level (1.0–10.0)",
        "metrics": {
            "cv_mae": round(results[winner]["cv_mae"], 4),
            "test_mae": round(test_mae, 4),
            "test_r2": round(test_r2, 4),
            "within_1_grade_pct": round(acc, 2),
        },
        "per_grade_mae": results[winner]["per_grade_mae"],
        "mae_gate": MAE_GATE,
        "mae_gate_passed": test_mae <= MAE_GATE,
        "compared_against": {
            loser: {
                "test_mae": round(results[loser]["test_mae"], 4),
                "test_r2": round(results[loser]["test_r2"], 4),
            }
        },
    }
    CARD_FILE.write_text(json.dumps(card, indent=2), encoding="utf-8")
    print(f"  Model card: {CARD_FILE}")

    print(f"\n=== TRAINING COMPLETE ===")


if __name__ == "__main__":
    main()
