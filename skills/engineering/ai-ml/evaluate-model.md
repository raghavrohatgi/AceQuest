# Skill: Evaluate ML Model

## Purpose
Define the standard procedure for evaluating machine learning models in AceQuest — including the IRT calibration, adaptive question selector, skill mastery estimator, and recommendation engine. Model evaluation is required before any model is deployed to production and after every retraining cycle. Evaluation covers predictive accuracy, calibration, fairness across grade/gender groups, and downstream impact on student learning outcomes.

## Used By
- AI/ML Agent
- Data Science Agent
- Product Agent (for go/no-go decision)

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| `modelType` | string | `"irt-calibration" \| "adaptive-selector" \| "recommendation" \| "mastery-estimator"` |
| `trainData` | DataFrame | Training dataset |
| `testData` | DataFrame | Held-out test dataset (never seen during training) |
| `baselineModel` | object | Previous production model for comparison |
| `fairnessGroups` | string[] | Demographic segments to check: `["grade", "gender", "school_type"]` |
| `productionThresholds` | object | Minimum acceptable metric values |

## Production Deployment Thresholds

| Model | Metric | Minimum | Target |
|-------|--------|---------|--------|
| IRT Calibration | RMSE (predicted P vs observed) | < 0.12 | < 0.08 |
| IRT Calibration | Item fit chi-sq (% misfitting items) | < 5% | < 2% |
| Adaptive Selector | Ability SE reduction / session | > 15% | > 25% |
| Adaptive Selector | AUROC (correct prediction) | > 0.70 | > 0.78 |
| Recommendation | Precision@5 | > 0.50 | > 0.65 |
| Recommendation | Recall@10 | > 0.40 | > 0.55 |
| Mastery Estimator | Mastery level accuracy | > 0.75 | > 0.85 |
| Mastery Estimator | RMSE vs expert-assigned levels | < 0.20 | < 0.12 |

## Procedure / Template

### Step 1 — Train/Test Split Strategy

```python
# evaluation/data_split.py
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit

def temporal_split(df: pd.DataFrame, test_weeks: int = 4) -> tuple:
    """
    Temporal split: use most recent weeks as test set.
    Prevents data leakage from future responses informing past ability estimates.
    """
    cutoff = df["submitted_at"].max() - pd.Timedelta(weeks=test_weeks)
    train = df[df["submitted_at"] < cutoff]
    test  = df[df["submitted_at"] >= cutoff]
    print(f"Train: {len(train)} responses | Test: {len(test)} responses")
    print(f"Train students: {train['student_id'].nunique()} | Test: {test['student_id'].nunique()}")
    return train, test

def student_split(df: pd.DataFrame, test_size: float = 0.20) -> tuple:
    """
    Student-level split: all responses from a student in the same split.
    Used for recommendation evaluation.
    """
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=42)
    train_idx, test_idx = next(splitter.split(df, groups=df["student_id"]))
    return df.iloc[train_idx], df.iloc[test_idx]
```

### Step 2 — IRT Calibration Evaluation

```python
# evaluation/irt_eval.py
import numpy as np
from sklearn.metrics import roc_auc_score, brier_score_loss
from irt.model import ThreePLModel, IRTParameters

def evaluate_irt(
    test_responses: np.ndarray,   # (n_students, n_items)
    theta: np.ndarray,            # (n_students,)
    item_params: list,            # list of IRTParameters
) -> dict:
    """Comprehensive IRT model evaluation."""

    a = np.array([p.a for p in item_params])
    b = np.array([p.b for p in item_params])
    c = np.array([p.c for p in item_params])

    p_hat = ThreePLModel.probability_vectorised(theta, a, b, c)

    mask = ~np.isnan(test_responses)
    observed = test_responses[mask]
    predicted = p_hat[mask]

    rmse = np.sqrt(np.mean((observed - predicted) ** 2))
    brier = brier_score_loss(observed, predicted)
    auroc = roc_auc_score(observed, predicted)

    # Expected Calibration Error (ECE): are predicted probabilities calibrated?
    ece = _compute_ece(observed, predicted, n_bins=10)

    # Item-level fit: % of items with significant misfit
    from irt.evaluation import item_fit_chisq
    chisq_stats = item_fit_chisq(test_responses, theta, a, b, c)
    misfit_pct = np.mean(chisq_stats > 20) * 100  # chi-sq(10) critical value ~18

    return {
        "rmse": round(float(rmse), 4),
        "brier_score": round(float(brier), 4),
        "auroc": round(float(auroc), 4),
        "ece": round(float(ece), 4),
        "item_misfit_pct": round(float(misfit_pct), 2),
        "n_students": int(theta.shape[0]),
        "n_items": int(len(item_params)),
        "n_responses": int(mask.sum()),
    }

def _compute_ece(observed, predicted, n_bins=10) -> float:
    """Expected Calibration Error."""
    bins = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        mask = (predicted >= bins[i]) & (predicted < bins[i+1])
        if mask.sum() == 0:
            continue
        acc = observed[mask].mean()
        conf = predicted[mask].mean()
        ece += mask.sum() / len(observed) * abs(acc - conf)
    return ece
```

### Step 3 — Recommendation Engine Evaluation

```python
# evaluation/recommendation_eval.py
import numpy as np
from collections import defaultdict

def precision_at_k(recommended: list, relevant: set, k: int) -> float:
    """Fraction of top-k recommendations that are relevant."""
    top_k = recommended[:k]
    return len(set(top_k) & relevant) / k

def recall_at_k(recommended: list, relevant: set, k: int) -> float:
    """Fraction of relevant items retrieved in top-k."""
    if not relevant:
        return 0.0
    top_k = recommended[:k]
    return len(set(top_k) & relevant) / len(relevant)

def ndcg_at_k(recommended: list, relevant: set, k: int) -> float:
    """Normalised Discounted Cumulative Gain."""
    dcg = sum(
        1 / np.log2(i + 2)
        for i, item in enumerate(recommended[:k])
        if item in relevant
    )
    idcg = sum(1 / np.log2(i + 2) for i in range(min(k, len(relevant))))
    return dcg / idcg if idcg > 0 else 0.0

def evaluate_recommendations(test_df, recommender, k_values=(5, 10)) -> dict:
    """
    test_df: DataFrame with columns [student_id, quiz_id, completed]
    Evaluates recommendations against actually completed quizzes (ground truth).
    """
    results = defaultdict(list)

    for student_id, group in test_df.groupby("student_id"):
        relevant = set(group[group["completed"] == 1]["quiz_id"])
        if not relevant:
            continue

        recommendations = recommender.recommend(student_id, n=max(k_values))

        for k in k_values:
            results[f"precision@{k}"].append(precision_at_k(recommendations, relevant, k))
            results[f"recall@{k}"].append(recall_at_k(recommendations, relevant, k))
            results[f"ndcg@{k}"].append(ndcg_at_k(recommendations, relevant, k))

    return {metric: round(np.mean(values), 4) for metric, values in results.items()}
```

### Step 4 — Fairness Evaluation

```python
# evaluation/fairness_eval.py
import pandas as pd
import numpy as np

def evaluate_fairness(
    predictions: pd.DataFrame,  # columns: student_id, grade_level, gender, predicted, observed
    protected_attributes: list[str],
    metric_fn,
) -> pd.DataFrame:
    """
    Compute metric disaggregated by protected attribute.
    Flags groups where metric deviates > 10% from overall metric.
    """
    overall = metric_fn(predictions["observed"], predictions["predicted"])
    rows = [{"group": "overall", "attribute": "all", "metric": overall, "gap": 0.0}]

    for attr in protected_attributes:
        for group_val, group_df in predictions.groupby(attr):
            group_metric = metric_fn(group_df["observed"], group_df["predicted"])
            gap = group_metric - overall
            rows.append({
                "group": str(group_val),
                "attribute": attr,
                "metric": round(group_metric, 4),
                "gap": round(gap, 4),
            })

    result = pd.DataFrame(rows)

    # Flag concerning gaps
    result["alert"] = result["gap"].abs() > 0.10

    return result

# Example usage
from sklearn.metrics import roc_auc_score

fairness_df = evaluate_fairness(
    predictions=test_data,
    protected_attributes=["grade_level", "gender", "school_type"],
    metric_fn=roc_auc_score,
)
print(fairness_df[fairness_df["alert"]])
```

### Step 5 — Evaluation Report Template

```markdown
# Model Evaluation Report: IRT Calibration v2.1
**Date:** 2025-06-01
**Evaluator:** AI/ML Agent
**Model:** 3-PL IRT, EM calibration
**Training data:** 2,847 students × 120 items, Jan–May 2025
**Test data:** 680 students × 120 items, last 4 weeks (temporal split)

## Summary
| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| RMSE | 0.083 | < 0.12 | ✓ Pass |
| AUROC | 0.761 | > 0.70 | ✓ Pass |
| ECE | 0.031 | < 0.05 | ✓ Pass |
| Item misfit % | 1.7% | < 5% | ✓ Pass |

## Fairness Analysis
| Group | AUROC | Gap vs Overall | Alert |
|-------|-------|----------------|-------|
| Overall | 0.761 | — | — |
| Grade 3 | 0.748 | -0.013 | No |
| Grade 5 | 0.778 | +0.017 | No |
| Grade 8 | 0.742 | -0.019 | No |
| Private school | 0.782 | +0.021 | No |
| Govt school | 0.731 | -0.030 | No |

**Note:** Govt school students show -3% AUROC gap — investigate if low item exposure
  (fewer questions answered) is limiting estimation quality.

## Recommendation
DEPLOY v2.1. All thresholds met. Monitor govt school cohort for 2 weeks post-deploy.
```

## Output
- Evaluation notebook (`notebooks/eval_<model>_<date>.ipynb`)
- Evaluation report (markdown, filed in model registry)
- Fairness analysis table with flagged groups
- Go/no-go recommendation with rationale

## Quality Checks
- [ ] Test data is held out before any model training — no leakage
- [ ] Temporal split used (not random) for sequential learning data
- [ ] All production thresholds met before deploy
- [ ] Fairness evaluated across grade, gender, school type — no group > 10% gap
- [ ] Comparison to baseline model included (is new model better?)
- [ ] Calibration (ECE) checked — predicted probabilities must be reliable
- [ ] Report includes data statistics: n_students, n_items, n_responses, date range
- [ ] Negative results documented — model NOT deployed if thresholds not met

## Example

```bash
$ python -m evaluation.run --model irt-calibration --test-data data/test_2025_05.parquet

Evaluating IRT Calibration Model...
  RMSE:           0.083  [threshold < 0.12]  ✓
  AUROC:          0.761  [threshold > 0.70]  ✓
  ECE:            0.031  [threshold < 0.05]  ✓
  Item misfit:    1.7%   [threshold < 5%]    ✓

Fairness analysis: No group gap > 10%

Result: ALL THRESHOLDS MET — RECOMMEND DEPLOY
Report saved to: reports/irt_calibration_eval_2025-06-01.md
```
