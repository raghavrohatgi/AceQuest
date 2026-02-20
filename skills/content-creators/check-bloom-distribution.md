# Skill: check-bloom-distribution

## Purpose
Given a batch of generated questions, calculate the actual Bloom's taxonomy distribution and compare against the grade-band targets. Flags if any level is more than 5% outside target. Run this after `generate-questions` and after `ai-qa-review` passes.

## Used By
- QA Reviewer Agent (Stage 3)
- Pipeline Coordinator (batch validation)

## Inputs

| Input | Type | Description |
|---|---|---|
| `questions` | JSON array | Array of question objects with `bloom_level` field |
| `grade_band` | string | `"1-3"` / `"4-6"` / `"7-10"` |
| `question_type_filter` | string | `"mcq"` / `"fitb"` / `"all"` — which types to include in count |

## Bloom's Targets

| Grade Band | remember | understand + apply | analyse + reason |
|---|---|---|---|
| 1-3 | 40% | 45% | 15% |
| 4-6 | 25% | 50% | 25% |
| 7-10 | 20% | 50% | 30% |

**Note:** `bloom_level` values `"understand"` and `"apply"` are counted together. `"analyse"` counts as the reasoning tier.

## Procedure

### Step 1: Count

```python
from collections import Counter

def check_bloom_distribution(questions: list, grade_band: str, filter_type: str = "all") -> dict:
    if filter_type != "all":
        questions = [q for q in questions if q["question_type"] == filter_type]

    total = len(questions)
    if total == 0:
        return {"error": "No questions to evaluate"}

    counts = Counter(q["bloom_level"] for q in questions)

    recall_pct = round(counts.get("remember", 0) / total * 100, 1)
    apply_pct = round((counts.get("understand", 0) + counts.get("apply", 0)) / total * 100, 1)
    reason_pct = round(counts.get("analyse", 0) / total * 100, 1)

    targets = {
        "1-3": {"remember": 40, "understand_apply": 45, "analyse": 15},
        "4-6": {"remember": 25, "understand_apply": 50, "analyse": 25},
        "7-10": {"remember": 20, "understand_apply": 50, "analyse": 30},
    }[grade_band]

    TOLERANCE = 5  # ±5% allowed

    flags = []
    if abs(recall_pct - targets["remember"]) > TOLERANCE:
        flags.append(f"RECALL off target: actual {recall_pct}%, target {targets['remember']}% (±{TOLERANCE}%)")
    if abs(apply_pct - targets["understand_apply"]) > TOLERANCE:
        flags.append(f"APPLY off target: actual {apply_pct}%, target {targets['understand_apply']}% (±{TOLERANCE}%)")
    if abs(reason_pct - targets["analyse"]) > TOLERANCE:
        flags.append(f"REASON off target: actual {reason_pct}%, target {targets['analyse']}% (±{TOLERANCE}%)")

    return {
        "total_questions": total,
        "grade_band": grade_band,
        "actual": {
            "remember": recall_pct,
            "understand_apply": apply_pct,
            "analyse": reason_pct
        },
        "targets": targets,
        "status": "PASS" if not flags else "NEEDS_REBALANCE",
        "flags": flags,
        "raw_counts": dict(counts)
    }
```

### Step 2: If NEEDS_REBALANCE

Identify which Bloom's level is over-represented and which is under-represented.

Send a correction prompt to the SME agent:

```
The question batch for {chapter_title} has a Bloom's distribution issue:

Actual: {recall}% recall / {apply}% apply / {reason}% reasoning
Target: {target_recall}% recall / {target_apply}% apply / {target_reason}% reasoning

Issues: {flags}

Please generate {n} additional questions at the {under-represented level} level to rebalance the batch.
Replace {n} questions at the {over-represented level} level from the batch — remove the weakest ones.

Provide the replacement questions in the same JSON schema.
```

## Output

A distribution report JSON:

```json
{
  "chapter": "ch04-exploring-magnets",
  "subject": "science",
  "grade": 6,
  "grade_band": "4-6",
  "total_questions": 51,
  "actual": {
    "remember": 24.5,
    "understand_apply": 51.0,
    "analyse": 24.5
  },
  "targets": {
    "remember": 25,
    "understand_apply": 50,
    "analyse": 25
  },
  "status": "PASS",
  "flags": [],
  "raw_counts": {
    "remember": 13,
    "understand": 14,
    "apply": 12,
    "analyse": 12
  }
}
```

## Quality Checks

- [ ] `status` is `PASS` before sending batch to human review
- [ ] If `NEEDS_REBALANCE`, correction questions are generated and the batch is re-checked
- [ ] Maximum 2 rebalance rounds — if still off after 2, flag for manual review

## Notes
- Run this on the full batch (MCQ + FITB + Match combined), not just MCQ.
- FITB and Match questions tend to fall heavily in "remember" — this is expected. Flag only if the MCQ-only distribution is off.
- For Math: separately check that at least 40% of questions test conceptual understanding (not just procedural computation).
