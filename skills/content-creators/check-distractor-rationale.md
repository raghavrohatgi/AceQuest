# Skill: check-distractor-rationale

## Purpose
Verify that every MCQ distractor (wrong answer option) has a meaningful, named student misconception in its `distractor_rationale` field. Catches generic or empty rationales before questions reach human review — because `distractor_rationale` is what powers the diagnostic report students see.

## Used By
- QA Reviewer Agent (Stage 3)

## Inputs

| Input | Type | Description |
|---|---|---|
| `questions` | JSON array | MCQ question objects from `generate-questions` or `revise-question` |
| `subject` | string | `math` / `english` / `science` |
| `grade` | integer | Target grade |

## What "Good" vs "Bad" Looks Like

### BAD distractor rationales (flag these):
```json
"distractor_rationale": {
  "A": "This is wrong",
  "C": "Incorrect answer",
  "D": "Student may confuse this"  // too vague
}
```

### GOOD distractor rationales (these are diagnostic):
```json
"distractor_rationale": {
  "A": "Student adds numerator and denominator separately (e.g. 1/2 + 1/3 = 2/5)",
  "C": "Student multiplies instead of adding the fractions",
  "D": "Student finds a common denominator but forgets to adjust the numerators"
}
```

Good rationales name the **specific computational or conceptual error** a student makes, not just "it's wrong."

## Prompt

```
You are a psychometrics reviewer checking distractor quality for diagnostic assessment questions.

For EACH MCQ question below, review the distractor_rationale for all 3 wrong options.

For each distractor, evaluate:
1. SPECIFIC — Does it name a concrete, specific student error or misconception? (Not "it's wrong" or "student may confuse")
2. REAL — Is this a misconception that real CBSE Grade {grade} students actually make?
3. DIAGNOSTIC — If a student picks this option, can we infer something meaningful about their misunderstanding?

Return a JSON array, one object per question:
{
  "question_id": "<id>",
  "status": "PASS" | "NEEDS_IMPROVEMENT",
  "distractor_issues": {
    "<option_letter>": "<what's wrong with this rationale and how to fix it>"
    // only include letters that have issues; omit if PASS
  },
  "improved_rationale_suggestion": {
    "<option_letter>": "<a better distractor_rationale for this option>"
    // provide suggestions for all flagged options
  }
}

Questions to review:
{mcq_questions_json}
```

## Output

A distractor QA report:

```json
[
  {
    "question_id": "sci-6-ch4-mcq-007",
    "status": "NEEDS_IMPROVEMENT",
    "distractor_issues": {
      "A": "Too vague — 'student may be confused' doesn't identify the misconception",
      "C": "Generic — 'wrong answer' tells us nothing diagnostic"
    },
    "improved_rationale_suggestion": {
      "A": "Student believes all metals are magnetic, forgetting that aluminium and copper are not",
      "C": "Student confuses magnetic field strength with the size of the magnet"
    }
  },
  {
    "question_id": "sci-6-ch4-mcq-012",
    "status": "PASS",
    "distractor_issues": {},
    "improved_rationale_suggestion": {}
  }
]
```

## Auto-Actions

```python
for result in distractor_qa:
    if result["status"] == "NEEDS_IMPROVEMENT":
        # Update the question's distractor_rationale with improved suggestions
        for option, suggestion in result["improved_rationale_suggestion"].items():
            question["distractor_rationale"][option] = suggestion
        question["review_notes"] = (question.get("review_notes") or "") + \
            " [Distractor rationale auto-improved by check-distractor-rationale skill]"
```

Note: Unlike `ai-qa-review`, this skill auto-applies the suggested improvements rather than sending back to the SME agent — it's a refinement, not a regeneration.

## Quality Checks

- [ ] 100% of MCQ questions have `distractor_rationale` populated (no nulls or empty objects)
- [ ] 0% of rationales use phrases like "it's wrong", "incorrect", "student may confuse" without specifics
- [ ] Every rationale names a specific error type:
  - Math: computational error (added when should multiply), procedural error (wrong formula), conceptual error (misunderstood definition)
  - Science: misconception (all metals are magnetic), confusion between similar concepts (weight vs mass)
  - English: reading error (took detail from wrong paragraph), vocabulary confusion (word has multiple meanings)

## Notes
- Run this skill on every MCQ batch before passing to human review — it takes seconds and significantly improves the diagnostic value of the questions.
- The improved rationales from this skill are provisional — human reviewers (Stage 4) should still verify them.
- Keep a running log of common bad rationale patterns to improve the `generate-questions` prompt over time.
