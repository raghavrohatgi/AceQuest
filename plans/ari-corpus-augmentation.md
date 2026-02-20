---
planStatus:
  planId: plan-ari-corpus-augmentation
  title: ARI Corpus Augmentation — Improve Model from MAE 1.5 to ≤ 0.8
  status: draft
  planType: improvement
  priority: high
  owner: raghavrohatgi
  stakeholders: []
  tags:
    - ari
    - corpus
    - nlp
    - model-training
    - data-quality
  created: "2026-02-19"
  updated: "2026-02-19T00:00:00.000Z"
  progress: 0
---
# ARI Corpus Augmentation Plan

> **Goal:** Improve model MAE from 1.497 → ≤ 0.8 by adding precisely graded external text to fill the gaps the NCERT corpus cannot close on its own.

---

## Problem Diagnosis

The current model (GradientBoosting, 12,087 segments, 7 features) has:

| Grade | MAE | Verdict |
| --- | --- | --- |
| 1 | 3.648 | Very poor — predicted as Grade 4-5 |
| 2 | 3.849 | Very poor |
| 3 | 3.091 | Very poor |
| 4 | 2.672 | Poor |
| 5 | 1.777 | Poor |
| 6 | 1.261 | Borderline |
| **7** | **0.713** | **✓ Passes gate** |
| **8** | **0.641** | **✓ Passes gate** |
| 9 | 1.208 | Borderline |
| 10 | 2.300 | Poor |

**Two distinct failure modes:**

### Failure Mode A — Grade 1–5: Too few segments + wrong text type
- Grades 1–5 have only 259–705 segments vs 1,500–2,400 for Grades 7–8
- NCERT textbooks at Classes 1–5 are heavily visual (picture-based) — most text is exercise questions and labels, not prose
- The prose that does exist is very short (1–2 sentences) — our 20-word minimum filter correctly excludes these, but leaves the grade under-represented
- **The model predicts Grade 1 text as Grade 4–5** because the vocabulary in a Class 1 math story problem overlaps heavily with Class 4–5

### Failure Mode B — Grade 4–7: Feature indistinguishability
- Mean `pct_rare_words` for Grades 4–7: 16.0%, 15.9%, 15.4%, 16.5% — essentially identical
- Mean sentence length: 14.13, 14.30, 14.29, 14.37 — nearly identical
- **Root cause:** NCERT's curriculum is deliberately written at consistent difficulty across these grades — the textbooks themselves don't ramp up linearly

---

## What Text to Add (Recommended Sources)

### Priority 1: CBSE Sample Papers (High value, free, immediately available)

CBSE publishes official Sample Question Papers for Classes 3–10. These contain reading comprehension passages and scenario descriptions that are:
- **Precisely graded** — written by CBSE for that exact class
- **Prose-heavy** — no visual/activity content
- **Varied register** — science scenarios, social studies extracts, English comprehension

**Where:** cbseacademic.nic.in → Sample Question Papers → English (Language and Literature / Core)

**Grades to prioritise:** 3, 4, 5, 6, 9, 10 (the worst performers)

**Expected yield:** 10–15 passages per grade × 200–400 words each = 2,000–6,000 words per grade

---

### Priority 2: NCERT Exemplar Problems (English prose portions)

NCERT Exemplar books (available as PDFs on ncert.nic.in) are supplementary books with:
- **More complex language** than standard textbooks — designed to challenge strong students
- **Excellent for Grades 6, 9, 10** — the borderline performers
- **Pure prose** introduction sections before the exercises

**Available for:** Science (6–10), Maths (6–12), Social Science (6–8)

**Expected yield:** 500–1,000 new segments for Grades 6–10

---

### Priority 3: Pratham ASER Reading Texts (Critical for Grades 1–4)

The ASER (Annual Status of Education Report) reading assessment uses graded texts specifically designed to test Indian children at each grade level. Pratham publishes these openly.

**Why these are uniquely valuable:**
- The ONLY Indian dataset where grade = measured reading ability, not curriculum level
- Texts at each grade are validated against actual reading performance of thousands of Indian children
- Covers Grades 1–5 explicitly, exactly our worst performers

**Where:** pratham.org → ASER materials → Reading level texts (English and Hindi)

**Expected yield:** 20–30 texts per grade for Grades 1–5, ~100–200 words each = 2,000–6,000 words per grade for Grades 1–5

**Impact:** This alone could cut Grades 1–5 MAE in half — ASER texts are purpose-built for exactly the problem we're solving

---

### Priority 4: Graded Readers from Indian Publishers

Indian children's publishers produce graded reading series explicitly labelled by class:

| Publisher | Series | Grades | Notes |
| --- | --- | --- | --- |
| Pratham Books | StoryWeaver platform | 1–5 | Creative Commons licence — free to use |
| Oxford University Press India | Oxford Reading Tree (India edition) | 1–6 | Copyrighted — educational use only |
| Tulika Books | Level readers | 1–4 | Indian context, explicitly graded |
| NBT (National Book Trust) | Bal Sahitya | 3–8 | Government of India — public domain |

**Best option for legal/free use:** Pratham Books StoryWeaver — thousands of Indian children's stories at explicit reading levels (Levels 1–5 map to roughly Grades 1–5), all under Creative Commons CC-BY 4.0.

**Where:** storyweaver.org.in → Level 1–5 English stories (filter by language = English)

**Expected yield:** 50–100 stories per level × 200–600 words = 10,000–60,000 words for Grades 1–5

**This is the highest-volume source for the hardest-to-fix grades**

---

### Priority 5: CBSE Class 10–12 Board Exam Reading Passages

These are reading comprehension passages from past CBSE board exams:
- **Officially at Class 10/12 level** — precise calibration
- **Prose-heavy** — long unseen passages (200–500 words each)
- **Very diverse topics** — science, society, culture, economics
- **Freely available** on LearnCBSE, Vedantu, BYJU'S study materials

**Impact:** Class 10 currently has MAE 2.3 — the model underestimates Class 10 text difficulty. These passages will anchor the top of the scale.

**Expected yield:** 50–100 passages × 300 words = 15,000–30,000 words for Grade 10

---

### Priority 6: Wikipedia Simple English vs English (Automated)

This is a programmatic source — no manual curation needed:

- **Simple English Wikipedia** is written for readers with basic English — calibrated ~Grade 3–5 level
- **Standard Wikipedia** science/biology/physics articles = Grade 9–12 level
- **Contrast:** Same topic, two clearly different difficulty levels → synthetic training pairs

**How to use:** Use `wikipedia` Python package to pull articles on NCERT topics (photosynthesis, fractions, magnetism) in both Simple and Standard versions → label Simple = Grade 4, Standard = Grade 9

**Expected yield:** 500–1,000 synthetic pairs, completely automated

**Legal:** Wikipedia CC-BY-SA 4.0 — free to use

---

## Data Addition Strategy

### Labelling approach for external text

External text needs a `grade` label. Use two strategies:

**A — Source-derived labels** (Priority 1, 2, 3, 5)
The source itself tells us the grade. CBSE Sample Paper Grade 6 → label = 6. ASER Level 2 → label = 2. No inference needed.

**B — FK-anchored labels for StoryWeaver** (Priority 4)
StoryWeaver uses "Level 1–5", not school grade. Map using FK grade equivalences validated against known NCERT passages:
- StoryWeaver Level 1 → Grade 1–2 (FK 1.0–2.5)
- StoryWeaver Level 2 → Grade 2–3 (FK 2.5–3.5)
- StoryWeaver Level 3 → Grade 3–4 (FK 3.5–5.0)
- StoryWeaver Level 4 → Grade 5–6 (FK 5.0–6.5)
- StoryWeaver Level 5 → Grade 6–7 (FK 6.5–8.0)

**C — Wikipedia pairing** (Priority 6)
Simple English = Grade 4, Standard English topic article = Grade 9 (validated by FK as sanity check).

---

## Implementation Tasks

### Step A: Collect and ingest augmentation data

- [ ] **A1** Download CBSE Sample Papers (English) for Classes 3, 4, 5, 6, 9, 10 from cbseacademic.nic.in
  - Extract reading comprehension passages (unseen passages section)
  - Save as `/ari/augmentation/cbse-sample-papers/{grade}/passage-{n}.txt`
  - Target: 10–20 passages per grade

- [ ] **A2** Download Pratham ASER Level texts (Grades 1–5)
  - From pratham.org or aser.asercentre.org
  - Save as `/ari/augmentation/aser-texts/{level}/text-{n}.txt`
  - Target: 20–30 texts per level

- [ ] **A3** Scrape StoryWeaver stories (Levels 1–5, English)
  - Write `scripts/scrape_storyweaver.py` using StoryWeaver's public API
  - Filter: language = English, Level 1–5
  - Extract story text (body only — no title, author, metadata)
  - Save as `/ari/augmentation/storyweaver/{level}/story-{id}.txt`
  - Target: 50 stories per level minimum

- [ ] **A4** Download NCERT Exemplar PDFs for Classes 6, 9, 10
  - From ncert.nic.in → Exemplar Problems
  - Run Mistral OCR on these PDFs (same pipeline as Books-MD)
  - Extract only introduction/explanation sections (not exercise questions)
  - Save to `/ari/augmentation/ncert-exemplar/{grade}/`

- [ ] **A5** Pull Wikipedia article pairs on NCERT topics
  - Write `scripts/fetch_wikipedia_pairs.py`
  - Topics: photosynthesis, magnetism, fractions, democracy, water cycle, atoms, gravity
  - Pull both Simple English and standard English versions
  - Label Simple = Grade 4, Standard = Grade 9
  - Save to `/ari/augmentation/wikipedia/`

- [ ] **A6** Collect CBSE Board Exam reading passages (Grade 10)
  - Sources: LearnCBSE.in past papers (2018–2024), unseen reading comprehension passages
  - Save as `/ari/augmentation/board-exam-passages/grade-10/`
  - Target: 30–50 passages

### Step B: Build augmentation corpus

- [ ] **B1** Write `scripts/build_augmentation_corpus.py`:
  - Walk `/ari/augmentation/` directory
  - Apply same prose extraction logic as `corpus_builder.py`
  - Label each segment with grade and source tag
  - Output: `/ari/data/augmentation-labelled.jsonl`

- [ ] **B2** Merge with existing corpus:
  - Combine `corpus-labelled.jsonl` + `augmentation-labelled.jsonl`
  - Output: `/ari/data/corpus-combined.jsonl`
  - Print per-grade segment counts — target 800+ per grade

- [ ] **B3** Rebuild frequency list and vocab lists:
  - Run `build_frequency_list.py` on combined corpus
  - Run `build_vocab_lists.py` on combined corpus

- [ ] **B4** Re-extract features:
  - Run `extract_corpus_features.py` on combined corpus
  - Verify per-grade `pct_rare_words` now shows clearer trend (Grades 1–3 should be much lower than Grades 7–10)

### Step C: Retrain and evaluate

- [ ] **C1** Run `train_model.py` on combined feature matrix
  - Target: per-grade MAE improvements, especially Grades 1–5
  - Gate: Overall MAE ≤ 1.0 (relaxed from 0.8 given corpus structure)
  - Stretch goal: MAE ≤ 0.8

- [ ] **C2** Calibration check with held-out NCERT passages
  - Take 10 known-grade passages from Books-MD (not used in training)
  - Verify ARI scores within ±1 of true grade for Grades 1, 4, 6, 8, 10
  - If bias detected, apply min-max calibration

---

## Expected Impact by Source

| Source | Grades Helped | Expected MAE improvement |
| --- | --- | --- |
| ASER Level texts | 1, 2, 3 | High — currently ~0 data at true Grade 1-2 reading level |
| StoryWeaver stories | 1–5 | High — large volume, naturally graded prose |
| CBSE Sample Papers | 3–6, 9–10 | Medium — small volume but precisely labelled |
| NCERT Exemplar | 6, 9, 10 | Medium — harder than textbooks, anchors top of scale |
| Wikipedia pairs | 4, 9 | Medium — large volume, separates middle from upper |
| Board exam passages | 10 | Medium — anchors Grade 10, fixes underestimation |

**Predicted overall MAE after augmentation: 0.9–1.1** (down from 1.497)

To hit ≤ 0.8 per-grade, parse depth (spaCy v2 feature) will likely still be needed for Grades 4–7.

---

## Effort Estimate

| Task | Effort |
| --- | --- |
| A1–A3 (collection + scraping) | 2–3 hours |
| A4 Exemplar OCR | 0.5 hours (same Mistral pipeline) |
| A5–A6 (Wikipedia + board papers) | 1 hour |
| B1–B4 (build augmented corpus) | 1 hour |
| C1–C2 (retrain + evaluate) | 0.5 hours |
| **Total** | **\~5 hours** |

---

## Priority Order

If time is limited, do in this order:

1. **StoryWeaver stories (Levels 1–5)** — biggest volume, biggest impact on Grades 1–5
2. **ASER Level texts** — best calibrated for true Grade 1–3 difficulty
3. **CBSE Board Exam passages (Grade 10)** — fixes the top anchor
4. **Wikipedia pairs** — automated, no manual work
5. **CBSE Sample Papers** — fills Grades 3–6 gaps
6. **NCERT Exemplar** — fine-tuning the upper range

---

## Legal / Licence Summary

| Source | Licence | Commercial use OK? |
| --- | --- | --- |
| StoryWeaver stories | CC-BY 4.0 | ✅ Yes |
| Wikipedia / Simple Wikipedia | CC-BY-SA 4.0 | ✅ Yes (with attribution) |
| CBSE Sample Papers | Government of India — publicly released | ✅ Yes (educational) |
| ASER Level texts | Pratham — publicly shared | ✅ Yes (educational) |
| NCERT Exemplar | NCERT — government publication | ✅ Yes (non-profit educational use) |
| Board exam reading passages | CBSE — publicly published | ✅ Yes |

All sources are usable for building and publishing `ari-india` as an open-source tool.
