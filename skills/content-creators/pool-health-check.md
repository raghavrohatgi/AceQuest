# Skill: pool-health-check

## Purpose
Report the current state of the question bank for a given chapter or subject: pool sizes per concept, coverage percentage, how many questions are in each status, and which concepts are ready to go live vs blocked. Used before publishing and for ongoing monitoring.

## Used By
- Pipeline Coordinator (Stage 5, after publishing)
- Content Health Dashboard (continuous monitoring)

## Inputs

| Input | Type | Description |
|---|---|---|
| `subject` | string | `math` / `english` / `science` — or `"all"` for full report |
| `grade` | integer | Class number — or `0` for all grades |
| `chapter_number` | integer | Chapter number — or `0` for all chapters |

## Procedure

```python
def pool_health_check(subject: str, grade: int, chapter_number: int, db) -> dict:
    # Query all questions matching the filter
    questions = db.get_questions(
        subject=subject if subject != "all" else None,
        grade=grade if grade != 0 else None,
        chapter_number=chapter_number if chapter_number != 0 else None
    )

    # Group by pool_tag and status
    from collections import defaultdict, Counter
    pools = defaultdict(lambda: defaultdict(list))

    for q in questions:
        pools[q["pool_tag"]][q["status"]].append(q["id"])

    MIN_POOL_SIZE = 10
    results = []

    for pool_tag, statuses in pools.items():
        live = len(statuses.get("live", []))
        staged = len(statuses.get("staged", []))
        approved = len(statuses.get("human-approved", []))
        pending_illus = len(statuses.get("pending-illustration", []))
        in_review = len(statuses.get("ai-reviewed", []))
        draft = len(statuses.get("draft", []))
        needs_revision = len(statuses.get("needs-revision", []))
        rejected = len(statuses.get("rejected", []))
        verified = len(statuses.get("psychometrically-verified", []))

        total_available = live + staged + approved + pending_illus + verified
        ready_live = live + verified

        results.append({
            "pool_tag": pool_tag,
            "ready_live": ready_live,
            "is_live": ready_live >= MIN_POOL_SIZE,
            "pool_gap": max(0, MIN_POOL_SIZE - ready_live),
            "status_breakdown": {
                "live": live,
                "psychometrically_verified": verified,
                "staged": staged,
                "human_approved": approved,
                "pending_illustration": pending_illus,
                "in_ai_review": in_review,
                "draft": draft,
                "needs_revision": needs_revision,
                "rejected": rejected,
            },
            "total_ever_generated": sum(len(v) for v in statuses.values()),
            "rejection_rate": round(rejected / max(1, sum(len(v) for v in statuses.values())) * 100, 1)
        })

    # Summary
    live_pools = [r for r in results if r["is_live"]]
    blocked_pools = [r for r in results if not r["is_live"]]

    return {
        "filter": {"subject": subject, "grade": grade, "chapter": chapter_number},
        "summary": {
            "total_concepts": len(results),
            "live_concepts": len(live_pools),
            "blocked_concepts": len(blocked_pools),
            "coverage_pct": round(len(live_pools) / max(1, len(results)) * 100, 1)
        },
        "blocked_pools": [
            {"pool": r["pool_tag"], "gap": r["pool_gap"], "have": r["ready_live"]}
            for r in blocked_pools
        ],
        "all_pools": sorted(results, key=lambda r: r["ready_live"], reverse=True)
    }
```

## Output

```json
{
  "filter": { "subject": "science", "grade": 6, "chapter": 4 },
  "summary": {
    "total_concepts": 6,
    "live_concepts": 4,
    "blocked_concepts": 2,
    "coverage_pct": 66.7
  },
  "blocked_pools": [
    { "pool": "sci-6-ch4-magnetic-field", "gap": 3, "have": 7 },
    { "pool": "sci-6-ch4-everyday-uses", "gap": 6, "have": 4 }
  ],
  "all_pools": [
    {
      "pool_tag": "sci-6-ch4-magnetic-materials",
      "ready_live": 14,
      "is_live": true,
      "pool_gap": 0,
      "status_breakdown": {
        "live": 12,
        "psychometrically_verified": 2,
        "staged": 0,
        "human_approved": 0,
        "pending_illustration": 2,
        "in_ai_review": 0,
        "draft": 0,
        "needs_revision": 0,
        "rejected": 1
      },
      "total_ever_generated": 15,
      "rejection_rate": 6.7
    }
  ]
}
```

## Reading the Report

| Indicator | Meaning | Action |
|---|---|---|
| `coverage_pct < 100%` | Some concepts not yet live for students | Generate more questions for blocked pools |
| `pool_gap > 0` | Pool has fewer than 10 live questions | Run `generate-questions` targeting that concept; or approve staged/pending questions |
| `rejection_rate > 15%` | High rejection rate for a concept | Review the SME agent prompt for that subject/grade |
| `pending_illustration` high | Many questions waiting for images | Run illustration batch |
| `needs_revision` accumulating | QA revision backlog building up | Process revision batch via `revise-question` |

## Quality Checks

- [ ] Run after every `publish-to-bank` execution
- [ ] Target: `coverage_pct` ≥ 80% before a chapter's games go live to students
- [ ] Target: No concept with `pool_gap > 5` for live chapters
- [ ] Run weekly as a routine maintenance check across all published chapters

## Notes
- This skill is also the data source for the **Content Health Dashboard** in the review portal — the frontend reads this data and visualises it.
- Set up an automated alert: if any live concept's pool drops below 8 questions (due to retirements), trigger a new generation run for that concept automatically.
