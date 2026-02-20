# Skill: item-analysis

## Purpose
After a question has been answered by ≥ 500 students in-app, compute psychometric quality metrics (difficulty, discrimination, distractor effectiveness, skip rate). Flag questions that are outside target ranges for review, retirement, or revision. This is Stage 6 of the pipeline — it completes the feedback loop from student responses back to content quality.

## Used By
- Field Analysis Agent (Stage 6)

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `question_id` | string | The question ID |
| `response_data` | array | Array of student response records (see schema below) |
| `question` | object | The full question object from the question bank |

### Response Record Schema
```json
{
  "student_id": "uuid",
  "question_id": "sci-6-ch4-mcq-007",
  "selected_option": "A" | "B" | "C" | "D" | null,  // null = skipped
  "is_correct": true | false,
  "time_taken_seconds": 18,
  "hint_used": false,
  "session_id": "uuid",
  "student_grade": 6,
  "responded_at": "2026-03-01T10:23:00Z"
}
```

## Procedure

```python
from collections import Counter

def item_analysis(question: dict, response_data: list) -> dict:
    total = len(response_data)
    if total < 500:
        return {"status": "insufficient_data", "n": total}

    # Filter: only students in the target grade
    target_grade = question["grade"]
    responses = [r for r in response_data if r["student_grade"] == target_grade]
    n = len(responses)

    # --- Item Difficulty (p-value) ---
    correct = sum(1 for r in responses if r["is_correct"])
    p_value = round(correct / n, 3)

    # --- Skip Rate ---
    skipped = sum(1 for r in responses if r["selected_option"] is None)
    skip_rate = round(skipped / n, 3)

    # --- Distractor Effectiveness (MCQ only) ---
    option_counts = Counter(
        r["selected_option"] for r in responses if r["selected_option"] is not None
    )
    distractor_effectiveness = {}
    if question["question_type"] == "mcq":
        for option in ["A", "B", "C", "D"]:
            pct = round(option_counts.get(option, 0) / n * 100, 1)
            distractor_effectiveness[option] = pct

    # --- Item Discrimination Index ---
    # Upper 27% vs Lower 27% method
    sorted_by_session_score = sorted(responses, key=lambda r: r.get("session_score", 0), reverse=True)
    top_n = max(1, int(n * 0.27))
    top_group = sorted_by_session_score[:top_n]
    bottom_group = sorted_by_session_score[-top_n:]
    top_correct = sum(1 for r in top_group if r["is_correct"]) / top_n
    bottom_correct = sum(1 for r in bottom_group if r["is_correct"]) / top_n
    discrimination = round(top_correct - bottom_correct, 3)

    # --- Avg time ---
    times = [r["time_taken_seconds"] for r in responses if r.get("time_taken_seconds")]
    avg_time = round(sum(times) / len(times), 1) if times else None

    # --- Flag logic ---
    flags = []
    if p_value > 0.80:
        flags.append("TOO_EASY")
    if p_value < 0.30:
        flags.append("TOO_HARD")
    if discrimination < 0.20:
        flags.append("LOW_DISCRIMINATION")
    if skip_rate > 0.05:
        flags.append("HIGH_SKIP_RATE")
    if question["question_type"] == "mcq":
        for opt, pct in distractor_effectiveness.items():
            if opt != question["correct_answer"] and pct < 5.0:
                flags.append(f"NON_FUNCTIONING_DISTRACTOR_{opt}")

    # --- Determine new status ---
    if not flags:
        new_status = "psychometrically-verified"
    elif "TOO_EASY" in flags or "TOO_HARD" in flags:
        new_status = "flagged-difficulty"
    elif "LOW_DISCRIMINATION" in flags:
        new_status = "flagged-discrimination"
    elif "HIGH_SKIP_RATE" in flags:
        new_status = "flagged-clarity"
    else:
        new_status = "flagged-distractor"

    return {
        "question_id": question["id"],
        "n_responses": n,
        "item_difficulty": p_value,
        "item_discrimination": discrimination,
        "skip_rate": skip_rate,
        "distractor_effectiveness": distractor_effectiveness,
        "avg_time_seconds": avg_time,
        "flags": flags,
        "new_status": new_status,
        "action_required": _get_action(flags)
    }

def _get_action(flags: list) -> str:
    if not flags:
        return "none — promote to psychometrically-verified"
    if "TOO_EASY" in flags:
        return "send to human reviewer — increase difficulty or retire"
    if "TOO_HARD" in flags:
        return "send to human reviewer — simplify or check for ambiguity"
    if "LOW_DISCRIMINATION" in flags:
        return "send back to SME agent — question doesn't distinguish strong from weak students"
    if "HIGH_SKIP_RATE" in flags:
        return "send to language editor — question may be confusing or too long"
    if any("NON_FUNCTIONING_DISTRACTOR" in f for f in flags):
        return "update distractor — replace option chosen < 5% with a better alternative"
    return "review"
```

## Output

An item analysis record saved to the question bank and appended to:
`/content/analytics/item-analysis-<date>.json`

```json
{
  "question_id": "sci-6-ch4-mcq-007",
  "analysed_at": "2026-04-01T00:00:00Z",
  "n_responses": 634,
  "item_difficulty": 0.61,
  "item_discrimination": 0.38,
  "skip_rate": 0.02,
  "distractor_effectiveness": {
    "A": 12.3,
    "B": 61.2,
    "C": 18.4,
    "D": 8.1
  },
  "avg_time_seconds": 22.4,
  "flags": [],
  "new_status": "psychometrically-verified",
  "action_required": "none — promote to psychometrically-verified"
}
```

## Target Ranges Summary

| Metric | Target | Action if Outside |
| --- | --- | --- |
| Item difficulty (p-value) | 0.30–0.80 | TOO_EASY → review difficulty; TOO_HARD → simplify or retire |
| Item discrimination | ≥ 0.20 | LOW_DISCRIMINATION → SME agent revision |
| Skip rate | ≤ 5% | HIGH_SKIP_RATE → language editor |
| Distractor chosen | ≥ 5% per option | NON_FUNCTIONING → replace distractor |

## Diagnostic Mapping Output

For verified questions, update the question's `distractor_rationale` with real-world data:

```json
"distractor_effectiveness_observed": {
  "A": "12.3% of students chose this — confirms 'all metals are magnetic' misconception is common",
  "C": "18.4% chose this — confirms students confuse magnetic with metallic"
}
```

This data feeds into the student diagnostic report: if a student picks option A repeatedly, the app can confidently say "this student believes all metals are magnetic."

## Notes
- Run item analysis on a rolling basis: check every question once it has ≥ 500 attempts.
- Questions that are `psychometrically-verified` should still be re-analysed at 2,000 attempts to catch any drift (e.g. if questions leak online and students start searching for answers).
- Discrimination index requires `session_score` in response records — ensure the game engine logs total session score alongside each individual response.
