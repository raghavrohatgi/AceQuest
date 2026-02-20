# Skill: generate-passage

## Purpose
Author an original English comprehension passage on a given theme, check its readability, and generate 5 skill-differentiated questions. Used only by English agents. Passages must be entirely original — NCERT prose must NOT be reproduced.

## Used By
- English Teacher agents (Grades 1-3, 4-5, 6-8, 9-10)

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `theme` | string | Topic/theme for the passage (derived from chapter concepts) |
| `grade` | integer | Target grade level |
| `word_count_target` | integer | Target word count (see grade-band guide below) |
| `chapter_context` | string | Concept JSON summary — what the passage should relate to |

## Word Count & Readability Targets by Grade

| Grade | Word Count | Flesch-Kincaid Target | Sentence Length |
| --- | --- | --- | --- |
| 1-2 | 60–100 words | Grade 1–2 | ≤ 8 words |
| 3-4 | 100–150 words | Grade 3–4 | ≤ 12 words |
| 5-6 | 150–200 words | Grade 5–6 | ≤ 15 words |
| 7-8 | 200–280 words | Grade 7–8 | ≤ 20 words |
| 9-10 | 280–400 words | Grade 9–10 | ≤ 25 words |

## Step 1: Passage Authoring Prompt

```
You are a children's educational content writer creating original reading passages for Indian students.

Write an original passage on the theme: "{theme}"
Target grade: {grade}
Target word count: {word_count_target} words (±10%)
Context: This passage relates to the chapter concept: {chapter_context}

RULES:
- Write ENTIRELY ORIGINAL content — do not reproduce any NCERT text
- Use simple, clear language appropriate for Grade {grade}
- Include at least one Indian name, place, or context naturally in the passage
- Avoid complex vocabulary unless the word is being explicitly taught
- Make the passage engaging and informative — tell a mini-story or present facts in a narrative way
- End with a fact or thought that invites reflection

PASSAGE TYPE GUIDELINES:
[Grade 1-3]: Simple narrative or descriptive. One idea per sentence. No complex clauses.
[Grade 4-6]: Informational or narrative. May include comparisons. Use paragraphs.
[Grade 7-8]: Analytical or persuasive. Multiple paragraphs. Use topic sentences.
[Grade 9-10]: Discursive. May include data references, multiple perspectives, formal register.

Return the passage as plain text only — no title, no commentary.
```

## Step 2: Readability Check (run `readability-check` skill)

After generating the passage, run the `readability-check` skill to verify:
- Flesch-Kincaid grade level is within ± 1 of the target grade
- If outside range: regenerate with adjusted sentence length / vocabulary

## Step 3: Question Generation Prompt

Once the passage is approved, generate exactly 5 questions — one per skill level:

```
Below is a reading passage for Grade {grade} students.

Generate exactly 5 comprehension questions — one for each skill listed. Each question must test a DIFFERENT skill. All questions must be answerable from the passage only.

PASSAGE:
---
{passage_text}
---

Generate questions for these 5 skills in this order:
1. LITERAL RETRIEVAL — The answer is stated directly in the passage. Find and report.
2. INFERENCE — The answer is implied but not stated. The student must reason from clues.
3. VOCABULARY IN CONTEXT — Ask about the meaning of a specific word/phrase as used in the passage.
4. AUTHOR'S PURPOSE / TONE — Why did the author write this? What feeling does the passage convey?
5. TITLE / SUMMARY — Which title best fits this passage? Or: What is the main idea?

For each question, output:
{
  "skill": "literal | inference | vocabulary | author-purpose | summary",
  "question_text": "<question>",
  "options": ["A: ...", "B: ...", "C: ...", "D: ..."],
  "correct_answer": "A|B|C|D",
  "distractor_rationale": {
    "<wrong option letter>": "<why a student might pick this wrong answer>"
  },
  "explanation": "<why the correct answer is right and each wrong answer is wrong>",
  "bloom_level": "remember | understand | apply | analyse",
  "difficulty": "easy | medium | hard",
  "image_needed": null
}

Return a JSON array of 5 question objects.
```

## Output

Two outputs saved together:

### Passage record (`/content/passages/<subject>/class-<N>/passage-<id>.json`):
```json
{
  "passage_id": "eng-6-passage-001",
  "subject": "english",
  "grade": 6,
  "theme": "conservation of water",
  "chapter_reference": "ch04",
  "passage_text": "...",
  "word_count": 182,
  "flesch_kincaid_grade": 5.8,
  "is_original": true,
  "status": "draft",
  "questions": ["eng-6-p001-q1", "eng-6-p001-q2", "eng-6-p001-q3", "eng-6-p001-q4", "eng-6-p001-q5"]
}
```

### 5 question objects appended to the chapter question file:
`/content/questions/english/class-<N>/chapter-<N>-questions-draft.json`

## Quality Checks

- [ ] Passage word count within ±10% of target
- [ ] Flesch-Kincaid grade level within ±1 of target grade (run `readability-check`)
- [ ] Passage contains no NCERT text (check against source MD)
- [ ] All 5 questions test different skills (literal, inference, vocabulary, author-purpose, summary)
- [ ] Every distractor_rationale names a real reading error (e.g. "student picks detail from wrong paragraph")
- [ ] No question is answerable from general knowledge alone — must require the passage

## Notes
- Generate 4 passages per chapter for English (not just 1) to build a pool. Each passage covers a different concept or angle from the chapter.
- Passage review by a human is mandatory before questions are generated against it (see Stage 4 in the pipeline).
- For Grade 1-2: passages may be very short (6-10 sentences). Consider adding a `[DIAGRAM: simple illustration of the passage scene]` flag to signal that an image accompanies the passage in-app.
