# Skill: chapter-ingest

## Purpose
Read a Markdown chapter file from `/Books-MD/` and extract a structured concept JSON. This JSON is the input for `generate-questions` — it tells the SME agent exactly what concepts, objectives, and terms to cover, so question generation is focused and complete.

## Used By
- Pipeline Coordinator (Stage 1)

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `md_path` | string | Path to the chapter MD file (e.g. `/Books-MD/Science/Class-6/ch04-exploring-magnets.md`) |
| `subject` | string | `math` / `english` / `science` |
| `grade` | integer | Class number |
| `chapter_number` | integer | Chapter number within the book |

## Prompt

Send this prompt to Claude (Sonnet) with the full MD file content as context:

```
You are a curriculum analyst specialising in Indian CBSE/NCERT content.

Below is the text of an NCERT chapter in Markdown format.

Extract the following and return ONLY a valid JSON object (no commentary):

{
  "grade": <integer>,
  "subject": "<math|english|science>",
  "chapter_number": <integer>,
  "chapter_title": "<string>",
  "source_md": "<path to MD file>",
  "concepts": [
    "<concept 1>",
    "<concept 2>"
    // List every distinct concept taught in this chapter. Be specific.
    // e.g. "like poles repel" not just "magnets"
  ],
  "learning_objectives": [
    "<what a student should be able to DO after this chapter>"
    // Use action verbs: identify, calculate, explain, compare, classify
  ],
  "key_terms": [
    { "term": "<term>", "definition": "<simple definition a student would understand>" }
  ],
  "formulas_and_rules": [
    "<formula or rule in plain text or LaTeX>"
    // e.g. "Area of rectangle = length × breadth" or "$A = l \\times b$"
  ],
  "examples_from_book": [
    "<description of a worked example or activity in the chapter>"
  ],
  "diagrams_in_chapter": [
    "<description of each diagram or figure in the chapter>"
    // Extract from [DIAGRAM: ...] placeholders in the MD
  ],
  "common_student_misconceptions": [
    "<known misconception related to this chapter's content>"
    // These inform distractor design in question generation
  ],
  "grade_band": "<1-3|4-6|7-10>",
  "bloom_targets": {
    "remember": <integer percent>,
    "understand_apply": <integer percent>,
    "analyse_reason": <integer percent>
  }
}

Chapter MD content:
---
{CHAPTER_MD_CONTENT}
---
```

**Note on ****`bloom_targets`****:** Auto-populate based on grade:
- Grade 1-3: `{ "remember": 40, "understand_apply": 45, "analyse_reason": 15 }`
- Grade 4-6: `{ "remember": 25, "understand_apply": 50, "analyse_reason": 25 }`
- Grade 7-10: `{ "remember": 20, "understand_apply": 50, "analyse_reason": 30 }`

## Output

A JSON file saved at:
`/content/chapters/<subject>/class-<N>/chapter-<N>-concepts.json`

Example:
```json
{
  "grade": 6,
  "subject": "science",
  "chapter_number": 4,
  "chapter_title": "Exploring Magnets",
  "source_md": "/Books-MD/Science/Class-6/ch04-exploring-magnets.md",
  "concepts": [
    "magnetic and non-magnetic materials",
    "poles of a magnet (north and south)",
    "like poles repel, unlike poles attract",
    "magnetic field and field lines",
    "natural and artificial magnets",
    "uses of magnets in everyday life"
  ],
  "learning_objectives": [
    "Classify materials as magnetic or non-magnetic",
    "Identify the north and south poles of a magnet",
    "Predict the interaction between two magnets based on their poles",
    "Describe the shape of a magnetic field using field lines",
    "List everyday uses of magnets"
  ],
  "key_terms": [
    { "term": "magnet", "definition": "An object that attracts iron and certain metals" },
    { "term": "pole", "definition": "The end of a magnet where the magnetic force is strongest" },
    { "term": "magnetic field", "definition": "The area around a magnet where its force can be felt" }
  ],
  "formulas_and_rules": [
    "Like poles repel each other",
    "Unlike poles attract each other"
  ],
  "examples_from_book": [
    "Activity: testing which objects are attracted to a bar magnet",
    "Activity: using iron filings to show magnetic field lines"
  ],
  "diagrams_in_chapter": [
    "Bar magnet showing N and S poles with magnetic field lines",
    "Two magnets with like poles facing — showing repulsion",
    "Compass needle deflecting near a bar magnet"
  ],
  "common_student_misconceptions": [
    "All metals are magnetic (aluminium and copper are not)",
    "The north pole of a magnet points to the geographic north pole (actually it points to magnetic north, which is near the geographic south pole)",
    "Cutting a magnet in half removes one pole (actually each piece becomes a complete magnet with two poles)"
  ],
  "grade_band": "4-6",
  "bloom_targets": {
    "remember": 25,
    "understand_apply": 50,
    "analyse_reason": 25
  }
}
```

## Quality Checks

After generating the concept JSON, verify:
- [ ] `concepts` list has at least 4 entries (thin chapters may have fewer — that's OK)
- [ ] `learning_objectives` use action verbs (identify, explain, calculate, compare)
- [ ] `common_student_misconceptions` has at least 2 entries — if AI left it empty, add manually
- [ ] `bloom_targets` sum to 100
- [ ] `diagrams_in_chapter` entries match `[DIAGRAM: ...]` placeholders in the source MD

## Notes
- The `common_student_misconceptions` field is critical — it directly informs distractor design in `generate-questions`. If the AI doesn't surface good misconceptions, supplement with your own knowledge of the subject.
- Run this skill once per chapter. The concept JSON is stable — re-run only if the source MD file is significantly revised.
