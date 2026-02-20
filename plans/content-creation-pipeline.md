---
planStatus:
  planId: plan-content-creation-pipeline
  title: AceQuest — AI-Assisted Content Creation Pipeline
  status: draft
  planType: system-design
  priority: high
  owner: raghavrohatgi
  stakeholders: []
  tags:
    - content
    - ai
    - question-bank
    - cbse
    - ncert
    - pipeline
    - human-review
  created: "2026-02-17"
  updated: "2026-02-17T00:00:00.000Z"
  progress: 0
---
# AceQuest — AI-Assisted Content Creation Pipeline

> **Goal:** Systematically generate a high-quality, CBSE-aligned question bank for Grades 1-10 (Math, English, Science) using AI agents + human review, sourced from the NCERT books already stored in `/Books/`.

---

## What We Have

| Asset | Detail |
| --- | --- |
| **NCERT Books (PDFs)** | ~200 chapter PDFs across Math (Class 1, 2, 9, 10), English (Class 1, 2, 9, 10), Science (Class 6, 7, 8, 9, 10) stored in `/Books/` |
| **Books-MD (to create)** | Markdown conversion of all PDFs — canonical clean source for AI question generation, stored in `/Books-MD/` |
| **SME Agent Definitions** | 12 agents: 4 Math (Gr 1-3, 4-5, 6-8, 9-10), 4 English (same), 4 Science (same) in `/agents/content-creators/` |
| **JSON Question Format** | Defined in `README.md` — includes question, options, answer, explanation, difficulty, tags |
| **Indian Context Guide** | Names, currency, festivals, sports, food — baked into each agent |

---

## The Content Creation Pipeline

The pipeline has **7 stages**: PDF → MD → Ingest → Generate → Self-Review → Human Review → Publish → Field Analysis.

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ 0.CONVERT│→ │ 1.INGEST │→ │2.GENERATE│→ │ 3.AI QA  │→ │4. HUMAN  │→ │5.PUBLISH │→ │6. FIELD  │
│ PDF → MD │  │ MD → JSON│  │SME Agent │  │Self-check│  │  REVIEW  │  │  to DB   │  │ ANALYSIS │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

---

### Stage 0: Convert — PDF → Markdown (One-Time, Do First)

**Input:** Raw NCERT PDFs from `/Books/`
**Output:** Clean Markdown files in `/Books-MD/`

**Why do this first:**
- LLMs parse clean Markdown far better than raw PDF text (which has broken lines, OCR artefacts, garbled formulas)
- MD files become the **permanent, version-controlled source of truth** — run question generation as many times as needed without re-processing PDFs
- Allows manual fixes (formulas, table alignment, diagram descriptions) to be made once, not every generation run
- Smaller, cleaner context = fewer tokens per generation call = lower API cost

**Tool: Mistral OCR (****`mistral-ocr-latest`****)**

Why Mistral OCR over traditional PDF converters:
- Handles Hindi/Devanagari text correctly
- Describes embedded diagrams and images
- Outputs LaTeX for math formulas natively (critical for NCERT Math/Science)
- Reconstructs tables as Markdown tables (not flattened text)
- Handles multi-column NCERT layouts correctly
- Cost: ~$0.001/page → ~3,000 pages total → **\~$3 for all 200 chapters**

**Conversion script:**
```python
from mistralai import Mistral
import os, pathlib

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

def convert_pdf_to_md(pdf_path: str, output_path: str):
    with open(pdf_path, "rb") as f:
        result = client.ocr.process(
            model="mistral-ocr-latest",
            document={"type": "pdf", "data": f.read()}
        )
    md_content = "\n\n".join(page.markdown for page in result.pages)
    pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(md_content)
```

Run in parallel across all chapters using `concurrent.futures.ThreadPoolExecutor`.

**Output structure:**
```
/Books-MD/
├── Math/
│   ├── Class-1/
│   │   ├── ch01-let-us-sing.md
│   │   └── ch02-look-around.md
│   ├── Class-2/
│   ├── Class-9/
│   └── Class-10/
├── English/
│   ├── Class-1/
│   ├── Class-2/
│   ├── Class-9/
│   │   ├── Beehive/
│   │   └── Moments/
│   └── Class-10/
└── Science/
    ├── Class-6/
    ├── Class-7/
    ├── Class-8/
    ├── Class-9/
    └── Class-10/
```

**Volume:** ~200 chapter PDFs total. Can be batched and run in parallel (10-15 mins total).

**Output file location:** `/Books-MD/<Subject>/Class-<N>/<ch-title>.md`

---

### Stage 1: Ingest — MD → Concept JSON

**Input:** Markdown chapter files from `/Books-MD/`
**Output:** Structured concept JSON per chapter

**Output file location:** `/content/chapters/<subject>/class-<N>/chapter-<N>-concepts.json`

---

### Stage 2: Generate — SME Agent Creates Questions

**Input:** Chapter concept JSON from Stage 1 + source MD file from `/Books-MD/`
**Output:** Raw question bank JSON

**Process:**
- Feed each MD file to a "Chapter Analyst" prompt:
  *"Given this NCERT chapter in Markdown, extract: (a) key concepts, (b) learning objectives, (c) important terms with definitions, (d) formulas/rules, (e) examples used in the book, (f) a list of [DIAGRAM: ...] placeholders."*
- Save as structured JSON:

```json
{
  "grade": 6,
  "subject": "science",
  "chapter_number": 4,
  "chapter_title": "Exploring Magnets",
  "source_md": "/Books-MD/Science/Class-6/ch04-exploring-magnets.md",
  "concepts": ["magnetic materials", "poles of a magnet", "magnetic field"],
  "objectives": ["Identify magnetic and non-magnetic materials", "..."],
  "key_terms": [{ "term": "magnet", "definition": "..." }],
  "formulas": [],
  "diagrams_needed": ["Bar magnet with field lines", "Compass needle deflection"]
}
```


**Cognitive Demand Framework (Bloom's Distribution)**

Every generation run must hit these targets — AI defaults to recall if not explicitly constrained:

| Grade Band | Remember (Recall) | Understand/Apply | Analyse/Reason |
| --- | --- | --- | --- |
| Class 1-3 | 40% | 45% | 15% |
| Class 4-6 | 25% | 50% | 25% |
| Class 7-10 | 20% | 50% | 30% |

For Math specifically: distinguish **procedural fluency** (can compute) from **conceptual understanding** (knows why). Generate both types; do not let procedural dominate.

**Age-Differentiated Question Format Standards**

| Grade Band | Format Rules |
| --- | --- |
| Class 1-3 | Image-first: the question stem must work with a picture. Minimal reading required to answer. Short sentences only (≤12 words). No abstract text-only MCQ. |
| Class 4-6 | Mixed visual + text. Word problems must use familiar Indian contexts (market, cricket, festivals). |
| Class 7-10 | Text-dominant. Higher inference demand. Multi-step problems allowed. Case studies and assertion-reason questions. |

**Copyright Policy**

All generated questions must be **original** — not paraphrases of NCERT exercise questions. The MD source files are used for concept extraction and context only.
- ✅ Allowed: Original questions inspired by NCERT concepts
- ✅ Allowed: Adapting NCERT examples with changed numbers/names/context
- ❌ Not allowed: Reproducing NCERT exercise questions verbatim
- ❌ Not allowed: Using NCERT prose passages verbatim as assessment reading passages (must create original or use open-licensed passages for English comprehension)

For each chapter, run the matching SME agent with a structured prompt:

```
You are the [Grade X-Y] [Subject] Teacher agent.
Chapter: [Chapter Title] (Class N, NCERT)
Concepts to cover: [concept list from Stage 1]
Learning objectives: [objectives from Stage 1]
Grade band: [1-3 | 4-6 | 7-10]

Generate (pool size — 5x what will be shown to any one student):
- 30 MCQ questions at Bloom's distribution: [recall%] recall / [apply%] apply / [reason%] reasoning
- 15 Fill-in-the-Blank questions
- 6 Match-the-Following sets (5 pairs each)
- [English only] 4 original comprehension passages (≠ NCERT text) with 5 questions each

Rules:
- Every question must map to exactly one concept
- Questions must be ORIGINAL — not reproduced from NCERT exercises
- [Class 1-3] Every MCQ must include an IMAGE_NEEDED flag or be answerable from a picture
- For each MCQ, provide distractor_rationale: name the specific student misconception each wrong option targets
- Explanation must state: (a) why the correct answer is right, (b) why each distractor is wrong
- Use Indian names, contexts, currencies (₹), festivals, food, sports
- Flag image requirements: "IMAGE_NEEDED: [precise description]"

Output format: JSON array following the AceQuest question schema.
```

**Question Schema (extended with EI ASSET-grade fields):**
```json
{
  "id": "uuid",
  "subject": "math",
  "grade": 6,
  "chapter_number": 3,
  "chapter_title": "Playing with Numbers",
  "concept_tag": "factors-and-multiples",
  "question_type": "mcq | fitb | match | passage-mcq | dropdown",
  "difficulty": "easy | medium | hard",
  "bloom_level": "remember | understand | apply | analyse",
  "question_text": "...",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "B",
  "distractor_rationale": {
    "A": "Student confuses factors with multiples",
    "C": "Student lists divisors of the wrong number",
    "D": "Student includes 1 but excludes the number itself"
  },
  "explanation": "9 is a factor of 36 because 36 ÷ 9 = 4 exactly. Option A: 8 doesn't divide 36 evenly...",
  "image_needed": null,
  "is_original": true,
  "passage_id": null,
  "pool_tag": "ch03-factors",
  "exposure_count": 0,
  "retired": false,
  "status": "draft | ai-reviewed | human-approved | rejected",
  "generated_by": "agent-id",
  "reviewed_by": null,
  "review_notes": null,
  "item_difficulty": null,
  "item_discrimination": null,
  "created_at": "2026-02-17T00:00:00Z",
  "version": 1
}
```

**Volume targets per chapter (pool sizing at 5x):**
- MCQ: 30 questions (pool) → 6 shown per game session
- FITB: 15 questions (pool) → 3 shown per game session
- Match: 6 sets (pool) → 2 shown per game session
- English passages: 4 original passages × 5 questions = 20 passage questions
- Total pool: ~75 items per chapter → ensures no student sees the same question twice across 10+ sessions

**English Comprehension Passage Sub-Pipeline**

Passages require a separate workflow — they are not generated alongside questions:

1. **Passage authoring** (separate AI prompt): Generate an original 150-250 word passage on the chapter theme. Must NOT reproduce NCERT text.
2. **Readability check**: Verify Flesch-Kincaid grade level matches target grade ± 1
3. **Skill tagging**: Each question on the passage must test a different skill — literal retrieval, inference, vocabulary in context, author's purpose, title/summary
4. **Passage review**: Human reviewer checks passage independently before questions are generated against it

Passage schema:
```json
{
  "passage_id": "uuid",
  "subject": "english",
  "grade": 6,
  "theme": "conservation of water",
  "passage_text": "...",
  "word_count": 180,
  "flesch_kincaid_grade": 5.8,
  "is_original": true,
  "status": "draft | approved",
  "questions": ["uuid1", "uuid2", "uuid3", "uuid4", "uuid5"]
}
```

---

### Stage 3: AI Self-Review (Quality Gate 1)

**Input:** Raw questions from Stage 2
**Output:** Questions with AI-assigned QA flags

Run a separate "Reviewer Agent" over the generated questions:

```
You are a CBSE curriculum QA reviewer. For each question below, check ALL of the following:

ACCURACY
1. Is the correct answer factually correct per NCERT?
2. Are all distractors definitively wrong?

DISTRACTOR QUALITY
3. Does each distractor correspond to a real, named student misconception?
4. Are all 4 options plausibly attractive (no obviously silly distractors)?
5. Is there only one unambiguously correct answer?

COGNITIVE DEMAND
6. Does the bloom_level tag match the actual cognitive demand of the question?
7. Is this question testing understanding/application, or just recall of a fact?

LANGUAGE & AGE-FIT
8. Is the language age-appropriate for Grade [N]? (Use grade-band word lists)
9. Is the question stem unambiguous — could it be interpreted in more than one way?
10. Is the explanation sufficient for a student to understand WHY, not just WHAT?

ORIGINALITY
11. Is this question original (not a direct copy of an NCERT exercise)?

Flag each question: PASS | NEEDS_REVISION | REJECT
For NEEDS_REVISION and REJECT: specify which check failed and why.
```

**Auto-actions:**
- `PASS` → moves to Stage 4 (human review queue)
- `NEEDS_REVISION` → sent back to SME agent with the specific revision note (max 2 rounds)
- `REJECT` → logged and discarded; failure reason tracked to improve prompts

**Target:** 85%+ pass rate at this stage.

---

### Stage 4: Human Review (Quality Gate 2)

**The most critical stage.** No question reaches students without human sign-off. This is where diagnostic validity is assured.

**Reviewer Profiles (Tiered):**
- **Tier 1 — Subject Expert:** Validates factual accuracy and NCERT alignment. Retired CBSE teachers, IIT/NIT graduates. Paid ₹4/question reviewed.
- **Tier 2 — Language Editor:** Validates language clarity, grammar, age-appropriateness, cultural sensitivity. Paid ₹2/question reviewed.
- **Tier 3 — Pedagogy Reviewer:** Validates Bloom's tagging, distractor misconception rationale, explanation quality. Senior reviewer (first 500 questions only, then calibration maintains standard). Paid ₹3/question reviewed.

> For lean operations: Tier 1 and Tier 2 can be combined for one reviewer. Tier 3 is handled internally by the founder for the first 3 months.

**Reviewer Calibration (Do before any reviewer starts):**

Every new reviewer completes a calibration set of 20 pre-scored "gold standard" questions before entering the live queue. Their ratings are compared against the gold standard:
- Agreement ≥ 80% → Reviewer is onboarded
- Agreement 60-80% → One more calibration round with debrief
- Agreement < 60% → Not suitable; do not onboard

**Inter-Rater Reliability (First 200 questions):**

For the first 200 questions, two reviewers independently review each question. Disagreements are flagged and discussed to align the quality bar. Target inter-rater agreement: ≥ 85%.

**Reviewer Checklist:**
- [ ] Correct answer is factually correct (verified against NCERT source)
- [ ] Each distractor is definitively wrong — no ambiguity
- [ ] Each distractor_rationale names a real student misconception (not "it's wrong")
- [ ] Language is age-appropriate for the stated grade
- [ ] Question is unambiguous — one clear interpretation only
- [ ] Explanation teaches the concept, not just restates the answer
- [ ] Bloom's level tag is accurate
- [ ] No cultural insensitivity, bias, or stereotyping
- [ ] Question is original — not reproduced from NCERT exercises
- [ ] Image requirement (if flagged) is feasible and accurately described
- [ ] Difficulty rating is appropriate

**SLA:** Reviewers complete a batch of 30 questions in ≤ 75 minutes.

**Payout model:** ₹6/question total (₹4 subject + ₹2 language) → 1,000 approved questions = ₹6,000

---

### Stage 5: Publish to Production Database

**Input:** Human-approved questions (`status: "human-approved"`)
**Output:** Live question bank accessible by the game engine

**Process:**
- Questions with `status: "human-approved"` are promoted to the production DB
- Any IMAGE_NEEDED questions go to a separate illustration queue (illustrator creates the image, uploads it, question gets linked)
- Question bank is versioned — each question gets a `version` field so future edits are tracked
- Questions are organised into **pools per concept** — the game engine draws from the pool, never showing the same question to the same student twice
- A "Content Health Dashboard" shows: total questions per subject/grade/chapter, pool size, coverage %, items pending in review, items pending illustration

**Item Bank / Exposure Control:**
- Each question tracks `exposure_count` (how many students have seen it)
- Questions with exposure_count > 500 are flagged for review (risk of memorisation/leakage)
- Questions can be `retired: true` and replaced with fresh pool items
- Minimum pool size per concept: 10 approved questions before a concept appears in games

---

### Stage 6: Field Analysis — Item Quality Loop

**Input:** In-app response data after each question has been attempted by ≥ 500 students
**Output:** Flagged questions for retirement or revision; validated items promoted to "verified" status

This is what separates a diagnostic assessment platform from a quiz app. After real students answer questions, the data tells you whether each question is actually working.

**Metrics tracked per question:**

| Metric | Formula | Target Range | Action if Outside Range |
| --- | --- | --- | --- |
| **Item Difficulty (p-value)** | % of students who answered correctly | 0.30 – 0.80 | Flag for review: too easy (>0.80) or too hard (<0.30) |
| **Item Discrimination Index** | Correlation between this question score and total test score | ≥ 0.20 | Flag for revision if < 0.20 (question doesn't distinguish strong from weak students) |
| **Distractor Effectiveness** | % of students choosing each wrong option | Each distractor chosen by ≥ 5% | Replace non-functioning distractors (chosen < 5% = students see through it) |
| **Skip Rate** | % of students who skipped/timed out | < 5% | Flag for clarity review if > 5% |
| **Correct-on-first-attempt rate** | % who got it right without hints | Tracked for adaptive difficulty tuning |

**Auto-actions:**
- p-value outside 0.30–0.80 → `status: "flagged-difficulty"` → back to human reviewer
- Discrimination < 0.20 → `status: "flagged-discrimination"` → back to SME agent for revision
- Skip rate > 5% → `status: "flagged-clarity"` → language review
- All metrics in range after 500 attempts → `status: "psychometrically-verified"`

**Diagnostic Mapping (Core Product Value):**

Each verified question's distractor data is used to generate the student diagnostic report:
- If a student consistently picks the distractor tagged "adds numerators AND denominators separately", the system reports: *"Rohan adds the denominator when adding fractions — a common misconception. Recommended: play Fractions Foundations game."*
- This is only possible because every distractor has a `distractor_rationale` field from Stage 2.

---

## Content Coverage Roadmap

### Phase 1 — Launch Content (Month 1-2)
Focus on the grades/subjects we have books for AND that match our B2C target (Grades 3-8):

| Subject | Grades | Chapters to Cover | Target Questions |
| --- | --- | --- | --- |
| Math | 6 | 12 chapters (all of Class 6) | ~360 questions |
| English | 6 | Beehive + Moments (9+9 chapters) | ~540 questions |
| Science | 6 | 12 chapters (all of Class 6) | ~360 questions |
| **Total Phase 1** |  | **42 chapters** | **\~1,260 questions** |

This gives us enough for ~40-50 playable games at launch (30 questions per game).

### Phase 2 — Expand (Month 3-4)
- Add Class 7, 8 for all three subjects
- Add Class 5 Math + English
- Target: +2,000 questions → ~100 games total

### Phase 3 — Full Grades 3-10 (Month 5-6)
- Complete Classes 3, 4, 9, 10
- Hindi language variants for Phase 1 content
- Target: +3,000 questions → 200+ games

---

## Image Production Workflow

Many questions (especially Science diagrams, Math geometry, English picture comprehension) need images. Separate track:

1. During AI generation, any question needing an image is flagged: `"image_needed": "diagram of a plant cell with nucleus and cell wall labelled"`
2. Image requests are batched into weekly illustration jobs
3. Sources (in order of preference):
  - **AI-generated:** Midjourney/DALL-E for simple illustrations
  - **NCERT originals:** Many diagrams are openly available under government copyright; can use directly
  - **Commissioned:** Freelance illustrators for custom content (₹200-500 per image)
4. Images stored in `/content/images/<subject>/<grade>/` with filenames matching question IDs
5. Question record updated with `image_url` when image is ready

---

## Review Portal — Screen Spec

A minimal internal web tool (not in the main app). Screens needed:

### Review Dashboard
- Summary cards: Pending review | Approved today | Rejected today | Total in DB
- Filter by: Subject / Grade / Chapter / Reviewer
- Queue list: newest batches first

### Question Review Card
```
┌────────────────────────────────────────────────┐
│  Math · Grade 6 · Chapter 3: Playing with     │
│  Numbers · Concept: Factors                    │
│  Difficulty: Medium · Type: MCQ                │
├────────────────────────────────────────────────┤
│  Q: Which of the following is a factor of 36?  │
│                                                │
│  A) 8    B) 9    C) 10    D) 14               │
│                                                │
│  Correct Answer: B (9)                         │
│                                                │
│  Explanation: 36 ÷ 9 = 4 (no remainder).      │
│  8: 36÷8 = 4.5 (not exact). 10: 36÷10 = 3.6. │
│  14: 36÷14 = 2.57.                             │
├────────────────────────────────────────────────┤
│  AI QA Note: PASS                              │
├────────────────────────────────────────────────┤
│  [✅ Approve]  [✏️ Edit]  [❌ Reject]           │
│  Notes: ___________________________________    │
└────────────────────────────────────────────────┘
```

### Batch Management
- Create batch → assign to reviewer → track completion
- Export approved questions to production DB (one click)

---

## Tech Stack for the Pipeline

| Component | Tool |
| --- | --- |
| PDF → Markdown conversion | Mistral OCR (`mistral-ocr-latest`) — handles formulas, tables, Hindi text |
| MD files (canonical source) | `/Books-MD/` directory, version-controlled |
| AI generation | Claude API (Sonnet 4.5) with SME agent system prompts |
| AI QA review | Claude API (Haiku for cost efficiency) |
| Question storage | PostgreSQL with JSON column for question data |
| Review portal | Next.js + simple auth (internal only) |
| Image storage | AWS S3 or Cloudflare R2 |
| Production DB | Same PostgreSQL, `status` field gates live visibility |

---

## Cost Estimates

| Activity | Volume | Unit Cost | Total |
| --- | --- | --- | --- |
| PDF → MD conversion (Mistral OCR) | ~3,000 pages | ~$0.001/page | ~$3 (~₹250) |
| AI question generation (Claude Sonnet) | 7,500 questions (5x pool) | ~₹0.5/question | ~₹3,750 |
| AI QA pass (Claude Haiku) | 7,500 questions | ~₹0.1/question | ~₹750 |
| Human review — Subject expert (Tier 1) | 5,000 approved questions | ₹4/question | ~₹20,000 |
| Human review — Language editor (Tier 2) | 5,000 approved questions | ₹2/question | ~₹10,000 |
| Reviewer calibration sets | 3 reviewers × 20 questions | ₹0 (internal) | — |
| Image generation (AI) | 500 images | ~₹5/image | ~₹2,500 |
| **Total for 5,000 approved questions** |  |  | **\~₹37,250 (\~$450)** |

Still very low cost vs a traditional content team. The higher human review cost (vs original plan) reflects proper Tier 1 + Tier 2 review — necessary for diagnostic accuracy.

---

## Quality Metrics to Track

**Pipeline Health**

| Metric | Target |
| --- | --- |
| AI self-review pass rate | ≥ 85% |
| Human approval rate (Tier 1) | ≥ 80% of AI-passed questions |
| Inter-rater agreement (first 200 questions) | ≥ 85% |
| Average revision rounds per question | ≤ 1.2 |
| Pool size per concept before going live | ≥ 10 approved questions |
| Bloom's distribution (actual vs target) | Within ±5% of grade-band targets |
| Distractor rationale coverage | 100% of MCQ distractors have a named misconception |

**Item Quality (Post-Launch)**

| Metric | Target | Action |
| --- | --- | --- |
| Item difficulty (p-value) | 0.30 – 0.80 | Flag and retire outliers |
| Item discrimination index | ≥ 0.20 | Revise if below threshold |
| Non-functioning distractors | < 5% of options chosen by < 5% of students | Replace distractor |
| Student skip rate | < 5% per question | Clarity review |
| % questions reaching "psychometrically-verified" | ≥ 70% of published items | Continuous improvement |

---

## Next Steps

1. **Convert PDFs → Markdown** — Run all `/Books/` chapters through Mistral OCR to produce `/Books-MD/`. ~200 files, batch in parallel. One-time effort.
2. **Build the Chapter Ingest Script** — MD → concept JSON for all chapters in `/Books-MD/`
3. **Run pilot generation** — Pick 1 chapter (e.g., Science Class 6, Chapter 4: Exploring Magnets). Generate 75-question pool. Validate Bloom's distribution and distractor rationale quality.
4. **Calibrate prompts** — Review AI output against cognitive demand targets; adjust SME agent prompts until Bloom's distribution is on-target
5. **Build calibration set** — Curate 20 "gold standard" questions with annotated correct reviews. Used to onboard every human reviewer.
6. **Build Review Portal** — Minimal Next.js internal tool with Tier 1/Tier 2 reviewer lanes, checklist enforcement, inter-rater tracking
7. **Hire and calibrate reviewers** — 2 subject experts (Tier 1), 1 language editor (Tier 2). Run calibration before live review.
8. **Launch field analysis tracking** — Instrument the game engine to record per-question response data; build the item analysis dashboard
9. **Scale** — Once pilot chapter is fully verified (including field analysis on 500 student attempts), run all Phase 1 chapters in parallel

---

## Related Plans

- [student-experience-next-phase.md](./student-experience-next-phase.md) — What students experience after content is live
- [app-flow-and-gaps.md](./app-flow-and-gaps.md) — Full screen flow (content feeds into game engine here)
