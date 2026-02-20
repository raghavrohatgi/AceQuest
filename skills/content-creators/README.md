# Content Creator Skills

Reusable, composable procedures that the content-creator agents call to perform their work.

**Skills are the "how" — agents are the "who".**

Each skill file defines:
- What the skill does (purpose)
- What inputs it needs
- The exact prompt or procedure to execute
- What output to expect
- Which agents use it

---

## Skill Index

### Pipeline Skills (Stage 0–2)

| Skill | Stage | Used By | Purpose |
| --- | --- | --- | --- |
| [pdf-to-markdown.md](./pdf-to-markdown.md) | 0 | Pipeline coordinator | Convert a NCERT PDF chapter to clean Markdown via Mistral OCR |
| [validate-markdown.md](./validate-markdown.md) | 0 | PDF-to-MD agent | Validate OCR output for structural integrity and garbled text |
| [chapter-ingest.md](./chapter-ingest.md) | 1 | Pipeline coordinator | Extract concept JSON from a Markdown chapter file |
| [generate-questions.md](./generate-questions.md) | 2 | All 12 SME agents | Generate a full question pool (MCQ, FITB, Match) for a chapter |
| [generate-passage.md](./generate-passage.md) | 2 | English agents only | Author an original comprehension passage with readability check |

### Quality Assurance Skills (Stage 3)

| Skill | Stage | Used By | Purpose |
| --- | --- | --- | --- |
| [ai-qa-review.md](./ai-qa-review.md) | 3 | QA reviewer agent | Run 11-point QA check over a question batch |
| [check-bloom-distribution.md](./check-bloom-distribution.md) | 3 | QA reviewer agent | Verify Bloom's distribution matches grade-band targets |
| [check-distractor-rationale.md](./check-distractor-rationale.md) | 3 | QA reviewer agent | Verify every MCQ distractor has a named misconception |
| [readability-check.md](./readability-check.md) | 3 | English agents | Check Flesch-Kincaid grade level of a passage |
| [revise-question.md](./revise-question.md) | 3 | All SME agents | Revise a question based on QA failure feedback |
Publishing & Management Skills (Stage 5–6)
| Skill | Stage | Used By | Purpose |
| --- | --- | --- | --- |
| [publish-to-bank.md](./publish-to-bank.md) | 5 | Pipeline coordinator | Promote approved questions to live question bank |
| [pool-health-check.md](./pool-health-check.md) | 5 | Pipeline coordinator | Report pool size, coverage, and readiness per concept |
| [item-analysis.md](./item-analysis.md) | 6 | Field analysis agent | Compute psychometric metrics from student response data |

---

## How Skills Relate to Agents

```
Pipeline Coordinator
  ├── uses: pdf-to-markdown
  ├── uses: validate-markdown
  ├── uses: chapter-ingest
  ├── uses: publish-to-bank
  └── uses: pool-health-check

SME Agents (Math / English / Science × 4 grade bands each)
  ├── uses: generate-questions
  ├── uses: generate-passage  (English only)
  └── uses: revise-question

QA Reviewer Agent
  ├── uses: ai-qa-review
  ├── uses: check-bloom-distribution
  ├── uses: check-distractor-rationale
  └── uses: readability-check  (English passages)

Field Analysis Agent
  └── uses: item-analysis
```

---

## Skill File Format

Every skill file follows this structure:

```markdown
# Skill: [skill-name]

## Purpose
What this skill does and why it exists.

## Used By
Which agents invoke this skill.

## Inputs
What information must be provided to run this skill.

## Prompt / Procedure
The exact prompt text or step-by-step procedure.

## Output
What the skill returns (format, schema, file).

## Quality Checks
How to verify the skill ran correctly.

## Example
A worked example showing input → output.
```
