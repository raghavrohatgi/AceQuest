# Skill: publish-to-bank

## Purpose
Promote human-approved questions from draft storage into the live production question bank. Organises questions into concept pools, handles image-pending questions separately, and updates the Content Health Dashboard.

## Used By
- Pipeline Coordinator (Stage 5)

## Inputs

| Input | Type | Description |
|---|---|---|
| `approved_questions` | JSON array | Questions with `status: "human-approved"` |
| `subject` | string | `math` / `english` / `science` |
| `grade` | integer | Class number |
| `chapter_number` | integer | Chapter number |

## Pre-Publish Checklist

Before publishing, verify:
- [ ] `status === "human-approved"` on all questions
- [ ] `is_original: true` on all questions
- [ ] `distractor_rationale` populated on all MCQ questions
- [ ] `explanation` non-empty on all questions
- [ ] Pool size per concept ≥ 10 before that concept's questions go live (run `pool-health-check` first)
- [ ] IMAGE_NEEDED questions: either image is attached, or they're moved to `pending-illustration` status

## Procedure

```python
def publish_to_bank(approved_questions: list, db_connection) -> dict:
    published = []
    pending_illustration = []
    skipped = []

    for q in approved_questions:
        # Gate 1: Status check
        if q["status"] != "human-approved":
            skipped.append({"id": q["id"], "reason": f"Status is {q['status']}, not human-approved"})
            continue

        # Gate 2: Image check
        if q.get("image_needed") and not q.get("image_url"):
            q["status"] = "pending-illustration"
            pending_illustration.append(q)
            # Save to illustration queue — not yet live
            db_connection.save_to_illustration_queue(q)
            continue

        # Gate 3: Pool minimum check
        pool_tag = q["pool_tag"]
        current_pool_size = db_connection.count_live_questions(pool_tag=pool_tag)
        if current_pool_size + 1 < 10:
            # Stage but don't activate — wait for pool to reach minimum
            q["status"] = "staged"
            db_connection.upsert_question(q)
            # Will be activated by pool-health-check when minimum is reached
            continue

        # Promote to live
        q["status"] = "live"
        q["published_at"] = datetime.utcnow().isoformat() + "Z"
        db_connection.upsert_question(q)
        published.append(q["id"])

    return {
        "published": len(published),
        "pending_illustration": len(pending_illustration),
        "staged_awaiting_pool_minimum": len(approved_questions) - len(published) - len(pending_illustration) - len(skipped),
        "skipped": len(skipped),
        "skipped_reasons": skipped
    }
```

## Illustration Queue Workflow

Questions with `image_needed` set but no `image_url` are saved to a separate illustration queue.

The weekly illustration batch process:
1. Pull all `status: "pending-illustration"` questions
2. Group `image_needed` descriptions by subject/grade for efficiency
3. Generate or source images (AI-generated, NCERT originals, or commissioned)
4. Upload images to `/content/images/<subject>/class-<N>/<question_id>.<ext>`
5. Update `image_url` field on the question
6. Re-run publish: question now passes Gate 2 and goes live

## Output

A publish report:

```json
{
  "batch_id": "publish-2026-04-01-sci-6-ch4",
  "published_at": "2026-04-01T09:00:00Z",
  "subject": "science",
  "grade": 6,
  "chapter": 4,
  "published": 38,
  "pending_illustration": 7,
  "staged_awaiting_pool_minimum": 4,
  "skipped": 2,
  "skipped_reasons": [
    { "id": "sci-6-ch4-mcq-031", "reason": "Status is needs-revision, not human-approved" }
  ],
  "concept_pool_sizes": {
    "sci-6-ch4-magnetic-materials": 12,
    "sci-6-ch4-poles-of-magnet": 10,
    "sci-6-ch4-magnetic-field": 9,
    "sci-6-ch4-everyday-uses": 7
  },
  "concepts_not_yet_live": ["sci-6-ch4-everyday-uses"]
}
```

## Quality Checks

- [ ] Published count + pending + staged + skipped = total input count
- [ ] No `human-approved` questions left unpublished without an explicit reason
- [ ] Run `pool-health-check` after publishing to verify concept coverage

## Notes
- Questions with `status: "staged"` will be auto-promoted to `"live"` when their pool reaches 10. Run `pool-health-check` periodically to trigger this.
- Never publish directly to production without the pre-publish checklist. Even one factually incorrect question reaching students damages trust.
- Keep a publish log for audit purposes — record who approved and when for every published question.
