# Skill: generate-questions

## Purpose
Generate a full question pool (MCQ, FITB, Match) for a single chapter. This is the core content creation skill used by all 12 SME agents. Output is a JSON array of question objects conforming to the AceQuest question schema.

Pool is sized at 5x what any one student will see — so a student never sees the same question twice across multiple game sessions.

## Used By
- All 12 SME agents (Math, English, Science × 4 grade bands)
- Called after `chapter-ingest` has produced the concept JSON

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `concept_json` | object | Output of `chapter-ingest` skill |
| `chapter_md` | string | Full text of the source MD file |
| `agent_identity` | string | Which SME agent is generating (e.g. "Grade 6-8 Science Teacher") |

## Bloom's Distribution Targets

| Grade Band | Remember | Understand/Apply | Analyse/Reason |
| --- | --- | --- | --- |
| Class 1-3 | 40% | 45% | 15% |
| Class 4-6 | 25% | 50% | 25% |
| Class 7-10 | 20% | 50% | 30% |

## Prompt

```
You are the {agent_identity} for AceQuest, an Indian K-8 learning platform.

Your task: Generate a question pool for the chapter below. These questions will be used in diagnostic game assessments for CBSE students.

CHAPTER INFORMATION:
- Subject: {subject}
- Grade: {grade} (Grade band: {grade_band})
- Chapter: {chapter_number}. {chapter_title}
- Concepts to cover: {concepts list}
- Learning objectives: {objectives list}
- Common student misconceptions: {misconceptions list}
- Bloom's targets: {remember}% recall / {understand_apply}% apply / {analyse_reason}% reasoning

GENERATE THE FOLLOWING POOL:
- 30 MCQ questions (4 options each)
- 15 Fill-in-the-Blank (FITB) questions
- 6 Match-the-Following sets (5 pairs per set)

DISTRIBUTION RULES:
- Spread questions across ALL concepts listed — do not concentrate on one concept
- Hit Bloom's targets: {remember}% recall / {understand_apply}% apply / {analyse_reason}% reasoning
- Difficulty split across MCQ: 25% easy, 50% medium, 25% hard
- [Math only] Generate both procedural (can compute) AND conceptual (knows why) questions. Do not let procedural dominate.

GRADE-BAND FORMAT RULES:
[Class 1-3]: Every MCQ must be image-first — the question must work with a picture. Short sentences only (≤12 words). Mark IMAGE_NEEDED for every question stem.
[Class 4-6]: Mixed visual + text. Word problems must use Indian contexts (market, cricket, festivals, school).
[Class 7-10]: Text-dominant. Multi-step problems allowed. Include assertion-reason questions in the hard tier.

ORIGINALITY RULES:
- Questions must be ORIGINAL — do not reproduce NCERT exercise questions
- Adapting NCERT examples with changed numbers/names/contexts is allowed
- Each question must map to exactly one concept from the concepts list

INDIAN CONTEXT REQUIREMENTS:
- Use Indian names: Priya, Arjun, Meena, Ravi, Ananya, Vikram, Kavya, Rohan
- Use Indian contexts: cricket, festivals (Diwali, Holi, Pongal), food (roti, dal, idli), places (Delhi, Mumbai, Chennai), currency ₹
- Avoid Western references unless the chapter content itself requires it

DISTRACTOR RULES (MCQ only):
- Each wrong option must correspond to a specific, predictable student error or misconception
- Name the misconception in distractor_rationale for each wrong option
- All 4 options must be plausibly attractive — no obviously silly distractors

IMAGE REQUIREMENTS:
- Flag image-dependent questions: "image_needed": "precise description of what image shows"
- [Class 1-3]: Every MCQ gets an image_needed flag
- [Class 4-6 Science/Math]: Flag questions involving diagrams, graphs, or geometry

OUTPUT FORMAT:
Return a JSON array. Each object must follow this schema exactly:

{
  "id": "generate a unique slug, e.g. sci-6-ch4-mcq-001",
  "subject": "{subject}",
  "grade": {grade},
  "chapter_number": {chapter_number},
  "chapter_title": "{chapter_title}",
  "concept_tag": "<one concept from the concepts list>",
  "question_type": "mcq" | "fitb" | "match",
  "difficulty": "easy" | "medium" | "hard",
  "bloom_level": "remember" | "understand" | "apply" | "analyse",
  "question_text": "<question stem>",
  "options": ["A: ...", "B: ...", "C: ...", "D: ..."],  // MCQ only
  "correct_answer": "A" | "B" | "C" | "D",             // MCQ: letter; FITB: the word/phrase
  "distractor_rationale": {                              // MCQ only
    "A": "<misconception this option targets if wrong>",
    "B": "<misconception>",
    "C": "<misconception>",
    "D": "<misconception>"
    // Only fill for the 3 wrong options; leave correct option as null or omit
  },
  "match_pairs": [                                       // Match only
    { "left": "...", "right": "..." }
  ],
  "blank_position": "<sentence with ___ for the blank>", // FITB only
  "explanation": "<why the correct answer is right> + <why each distractor is wrong (MCQ) or what the answer is (FITB)>",
  "image_needed": null | "<precise description of the image required>",
  "is_original": true,
  "pool_tag": "<subject>-<grade>-ch<chapter_number>-<concept_slug>",
  "exposure_count": 0,
  "retired": false,
  "status": "draft",
  "generated_by": "{agent_identity}",
  "reviewed_by": null,
  "review_notes": null,
  "item_difficulty": null,
  "item_discrimination": null,
  "created_at": "<ISO timestamp>",
  "version": 1
}

CHAPTER CONTENT FOR REFERENCE:
---
{chapter_md_content}
---
```

## Output

A JSON file saved at:
`/content/questions/<subject>/class-<N>/chapter-<N>-questions-draft.json`

Expected counts:
- 30 MCQ objects
- 15 FITB objects
- 6 Match objects (each with 5 pairs)
- Total: 51 question objects per chapter

## Quality Checks

After generation, run these checks before passing to `ai-qa-review`:
- [ ] Total count: 30 MCQ + 15 FITB + 6 Match = 51 objects
- [ ] All concepts from concept_json appear in at least 1 question's `concept_tag`
- [ ] No concept appears in more than 8 questions (no concept monopoly)
- [ ] MCQ `distractor_rationale` present for all 3 wrong options on every MCQ
- [ ] `explanation` field is non-empty and non-trivial on every question
- [ ] `is_original: true` on all questions
- [ ] Run `check-bloom-distribution` skill to verify Bloom's targets are met
- [ ] Run `check-distractor-rationale` skill to verify misconception quality

## Notes
- If a concept has very limited material (e.g. a short sub-section), it's OK to generate fewer questions for that concept and more for richer concepts. The total count matters, not equal distribution.
- For Math: explicitly label which questions are procedural vs conceptual in the `bloom_level` field (`apply` = procedural, `analyse` = conceptual reasoning).
- FITB questions should have exactly one correct answer. Avoid blanks where multiple answers are defensible.
