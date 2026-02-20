# Skill: ai-qa-review

## Purpose
Run an automated 11-point quality check over a batch of generated questions before they enter human review. Flags each question as PASS, NEEDS_REVISION, or REJECT with specific reasons. Reduces the human reviewer's workload by catching obvious errors first.

## Used By
- QA Reviewer Agent (Stage 3)

## Inputs

| Input | Type | Description |
|---|---|---|
| `questions_batch` | JSON array | Array of question objects from `generate-questions` output |
| `grade` | integer | Grade level (determines age-appropriateness standards) |
| `subject` | string | `math` / `english` / `science` |
| `concept_json` | object | Chapter concept JSON from `chapter-ingest` — used to verify concept alignment |

## Prompt

Use Claude (Haiku for cost efficiency). Process in batches of 10 questions per API call.

```
You are a CBSE curriculum QA specialist reviewing assessment questions for an Indian K-8 learning platform.

Grade: {grade}
Subject: {subject}
Chapter: {chapter_title}
Valid concepts for this chapter: {concepts_list}

For EACH question in the array below, evaluate ALL 11 checks and return a QA result.

=== THE 11 QA CHECKS ===

ACCURACY (must pass all)
1. FACTUAL_ACCURACY — Is the correct_answer factually correct per NCERT/CBSE standards?
2. DISTRACTORS_WRONG — Are all wrong options definitively incorrect? (No ambiguity where another option could also be right)

DISTRACTOR QUALITY (must pass all)
3. MISCONCEPTION_NAMED — Does each wrong option's distractor_rationale name a specific, real student misconception? (Reject if rationale just says "it's wrong" or is generic)
4. DISTRACTORS_PLAUSIBLE — Are all wrong options plausibly attractive? (Reject if any distractor is obviously silly or trivially wrong)
5. SINGLE_CORRECT — Is there exactly ONE unambiguously correct answer?

COGNITIVE DEMAND
6. BLOOM_ACCURATE — Does the bloom_level tag match the actual cognitive demand? (e.g. a question asking to recall a fact should be "remember", not "analyse")
7. NOT_PURE_RECALL — [For questions tagged understand/apply/analyse] Is this actually testing understanding, not just memorising a fact?

LANGUAGE & AGE-FIT
8. AGE_APPROPRIATE — Is the vocabulary and sentence complexity suitable for Grade {grade}? Flag if too complex or too simple.
9. UNAMBIGUOUS — Can the question stem be interpreted in only one way? Flag if a student could reasonably read it differently.
10. EXPLANATION_TEACHES — Does the explanation teach WHY (not just restate the answer)? Must explain why each distractor is wrong for MCQ.

ORIGINALITY
11. IS_ORIGINAL — Is this question original and not a direct copy of an NCERT exercise question?

=== OUTPUT FORMAT ===

Return a JSON array, one object per question:
{
  "question_id": "<id from input>",
  "flag": "PASS" | "NEEDS_REVISION" | "REJECT",
  "checks_failed": ["CHECK_NAME_1", "CHECK_NAME_2"],  // empty array if PASS
  "revision_note": "<specific instruction for SME agent on what to fix>",  // null if PASS
  "reject_reason": "<why this question cannot be fixed>",  // null unless REJECT
  "bloom_level_correction": "<correct bloom level if check 6 failed>",  // null otherwise
  "reviewer_note": "<optional note for human reviewer if question passes but has minor concerns>"
}

=== QUESTIONS TO REVIEW ===
{questions_json_array}
```

## Output

A QA results JSON file saved at:
`/content/questions/<subject>/class-<N>/chapter-<N>-qa-results.json`

And questions updated with QA status:
- `PASS` → `"status": "ai-reviewed"`
- `NEEDS_REVISION` → `"status": "needs-revision"` + revision note stored in `review_notes`
- `REJECT` → `"status": "rejected"` + reject reason logged

## Auto-Actions After QA

```python
for result in qa_results:
    if result["flag"] == "PASS":
        question["status"] = "ai-reviewed"
        # → moves to human review queue

    elif result["flag"] == "NEEDS_REVISION":
        question["status"] = "needs-revision"
        question["review_notes"] = result["revision_note"]
        question["revision_round"] = question.get("revision_round", 0) + 1
        if question["revision_round"] <= 2:
            # → send back to SME agent with revision_note via revise-question skill
            pass
        else:
            question["status"] = "rejected"
            question["review_notes"] = "Max revision rounds exceeded: " + result["revision_note"]

    elif result["flag"] == "REJECT":
        question["status"] = "rejected"
        question["review_notes"] = result["reject_reason"]
        # → logged, discarded, rejection reason tracked for prompt improvement
```

## Quality Checks (on the QA process itself)

- [ ] Pass rate ≥ 85% — if below, flag the SME agent prompt for revision
- [ ] NEEDS_REVISION reasons are specific enough for the SME agent to action (not vague)
- [ ] No REJECT on more than 5% of a batch — high reject rate signals a systematic prompt problem
- [ ] After running, also run `check-bloom-distribution` and `check-distractor-rationale` on the PASS batch

## Notes
- Use Claude Haiku (not Sonnet) for this skill to keep costs low — it's running checklist-style evaluation, not creative generation.
- Process in batches of 10 questions per call to avoid context length issues.
- Track failure patterns across batches: if CHECK 3 (MISCONCEPTION_NAMED) fails repeatedly, update the `generate-questions` prompt to be more explicit about distractor rationale.
