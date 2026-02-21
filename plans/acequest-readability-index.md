---
planStatus:
  planId: plan-acequest-readability-index
  title: AceQuest Readability Index (ARI)
  status: in-development
  planType: product
  priority: high
  owner: raghavrohatgi
  stakeholders: []
  tags:
    - readability
    - nlp
    - content-quality
    - indian-english
    - cbse
    - ncert
    - first-product
    - open-source
  created: "2026-02-18"
  updated: "2026-02-21T00:00:00.000Z"
  progress: 65
---
# AceQuest Readability Index (ARI)

> **Goal:** Build and release the first readability scoring system calibrated specifically on NCERT/CBSE Indian English content — as a standalone open-source product and paid API, before the AceQuest platform launches.

---

## Why ARI as First Product?

Releasing ARI first is strategically smart:

| Reason | Detail |
| --- | --- |
| **No platform dependency** | ARI is a pure NLP tool — can be built and shipped in ~3 weeks without any app infrastructure |
| **Market gap** | No Indian readability standard exists. Every ed-tech and publisher is solving this poorly or not at all |
| **Credibility builder** | Publishing a research-grade tool signals technical depth before AceQuest launches |
| **B2B revenue** | Ed-tech companies (BYJU'S, Vedantu, Toppr, publishers) will pay for a calibrated Indian readability API |
| **Open-source traction** | An open Python package with NCERT frequency lists will attract GitHub stars and press attention |
| **Fast feedback loop** | Real usage from other platforms validates/improves the model before AceQuest uses it internally |

---

## Why Build Our Own?

| Problem | Impact |
| --- | --- |
| **Lexile is US-calibrated** | Words like "panchayat", "dal", "krishi" are "rare" in an American corpus — unfairly penalises Indian content |
| **Flesch-Kincaid is formula-only** | Measures sentence length + syllables only. Doesn't account for vocabulary demand or conceptual density |
| **No Indian readability standard exists** | Every Indian ed-tech platform either uses Lexile (wrong calibration) or no readability check at all |
| **We have the corpus** | The `/Books-MD/` directory contains NCERT texts from Class 1–10 — a ready-made graded corpus |

---

## MVP Scope (First Release — v1)

Ship the smallest useful version. ARI v1 is a **Python package + hosted API** — no web UI, no dashboards, just the scoring engine.

### What's In (v1)
- Python package: `pip install ari-india`
- Single function: `ari.score(text, grade_band="4-6")` → returns ARI score + label
- NCERT word frequency list bundled (open-source data asset)
- REST API: `POST /score` → JSON response
- CBSE grade band support: 1-3, 4-6, 7-10
- English only

### What's Out (v1 — deferred to v2)
- Hindi support
- Subject-specific models (Math vs English vs Science)
- Parse depth / syntactic complexity feature
- Web dashboard / UI
- Batch processing endpoint

### Package Structure
```
ari-india/                     # Python package (PyPI)
├── ari/
│   ├── scorer.py              # Main scoring function
│   ├── features.py            # Feature extractor
│   ├── model.py               # Model loader + predictor
│   └── data/
│       ├── ncert-word-frequency.json
│       └── grade-vocab-lists.json
├── models/
│   └── ari-model-v1.pkl
├── tests/
├── README.md
└── setup.py

ari-api/                       # Hosted REST API (FastAPI)
├── main.py
├── Dockerfile
└── .env.example
```

---

## What ARI Measures

ARI is a regression model trained to predict CBSE grade level from text features. It outputs a score on a 1–10 scale mapping directly to Class 1–10.

### Input Features (what the model reads)

| Feature | Why It Matters |
| --- | --- |
| **Mean Word Frequency** (from NCERT corpus) | How common are the words? Rare words = harder. Uses an Indian corpus, not American. |
| **Mean Sentence Length** | Longer sentences = harder to parse |
| **Type-Token Ratio (TTR)** | Vocabulary diversity. Higher TTR = more varied, harder text |
| **Avg Syllables per Word** | Longer words tend to be more complex |
| **% Rare Words** | % of words not in the top-500 NCERT vocabulary for that grade band |
| **Avg Parse Depth** (optional, v2) | Syntactic complexity — how deeply nested are the clauses |
| **Concept Density** (optional, v2) | # of technical/domain terms per 100 words |

### Output

```
ARI Score: 5.3
→ "Suitable for Class 5 students (range: 5–6)"
```

AceQuest student-facing label: **"Quest Level 5"** — maps cleanly to the game's level aesthetic.

---

## Steps to Build ARI

### Pre-requisite: MD File Validation

Before corpus prep can start, the Mistral OCR-converted MD files must be validated. See the `validate-markdown.md` skill.

**Quick gate before corpus use:**
- [ ] YAML frontmatter present and parseable on all files
- [ ] Prose paragraphs correctly separated from exercises/headings
- [ ] No garbled text in ≥ 95% of paragraphs (spot-check 10% of files)
- [ ] Math formulas preserved (LaTeX) — exclude from prose corpus; include in concept density feature later
- [ ] Word count per chapter is plausible (Class 6 Science chapter: typically 1,500–3,000 words)

---

### Phase 1: Corpus Preparation (prerequisite: `/Books-MD/` conversion complete)

**Step 1.1 — Compile the graded corpus**
- Source: All chapter MD files in `/Books-MD/` (Math, English, Science, Classes 1–10)
- For each chapter, extract prose paragraphs only (exclude headings, tables, exercise questions, YAML frontmatter)
- Label each text segment with its grade: `{ "text": "...", "grade": 6 }`
- Target: 500–1,000 labelled text segments per grade level

**Step 1.2 — Build the NCERT word frequency list**
- Pool all prose text from all grades
- Count frequency of every word across the full corpus
- Produce a ranked frequency list: `{ "word": "magnet", "frequency": 234, "rank": 1820 }`
- Separate frequency lists per grade band (1-3, 4-6, 7-10) — this gives grade-specific "familiar word" baselines
- Output: `/ari/data/ncert-word-frequency.json`

**Step 1.3 — Build grade-level vocabulary lists**
- Top 500 most frequent words per grade band = "familiar vocabulary" for that band
- Words outside this list = "rare/challenging" for that grade
- Output: `/ari/data/grade-vocab-lists.json`

---

### Phase 2: Feature Extraction

**Step 2.1 — Write the feature extractor**

For a given text string, compute:

```
features = {
  mean_word_frequency_rank,     # avg rank of words in NCERT corpus (lower rank = more common)
  mean_sentence_length,          # avg words per sentence
  type_token_ratio,              # unique words / total words
  avg_syllables_per_word,        # proxy for word complexity
  pct_rare_words,                # % words not in top-500 for target grade band
  word_count                     # total words (useful but not a predictor)
}
```

**Step 2.2 — Extract features for all corpus segments**
- Run the feature extractor over every labelled text segment from Phase 1
- Output: `/ari/data/corpus-features.csv` (columns: grade + 5 feature columns)

---

### Phase 3: Model Training

**Step 3.1 — Train a regression model**

```python
# Simple linear regression or gradient boosted trees
# Input: 5 features
# Output: predicted grade level (1.0–10.0)
# Evaluation: Mean Absolute Error (MAE) — target ≤ 0.8 grade levels

from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
```

**Step 3.2 — Evaluate and select model**
- Split corpus 80/20 train/test
- Try: Ridge regression, Random Forest, Gradient Boosting
- Target metric: **MAE ≤ 0.8** (within 1 grade level 90% of the time)
- Output: `/ari/models/ari-model-v1.pkl`

**Step 3.3 — Calibrate the output scale**
- Map raw regression output to ARI 1–10 scale
- Verify that Class 6 NCERT text scores in 5.5–6.5 range consistently
- Generate a calibration table: known-grade passages → ARI scores

---

### Phase 4: Validation

**Step 4.1 — Internal validation**
- Test on held-out chapters (not used in training)
- Test on AceQuest-generated passages from `generate-passage` skill
- Target: 90% of passages score within ±1 of their target grade

**Step 4.2 — Expert validation**
- Share 20 test passages + ARI scores with 2 experienced CBSE English teachers
- Ask: "Does this difficulty level feel right for Grade X students?"
- Adjust calibration if teachers consistently disagree with ARI

**Step 4.3 — Cross-validate against FK**
- Compare ARI vs FK on same passages
- Document cases where they diverge — these are the interesting cases that show ARI's advantage (e.g. an NCERT-style verbose-but-simple sentence scoring too hard in FK but correctly easy in ARI)

---

### Phase 5: Release (First Product)

**Step 5.1 — Package and publish**
- Wrap feature extractor + trained model into `ari-india` Python package
- Publish to PyPI: `pip install ari-india`
- Publish GitHub repo with MIT licence
- Upload NCERT word frequency list to HuggingFace datasets

**Step 5.2 — Deploy API**
- Wrap in FastAPI: `POST /score { "text": "...", "grade_band": "4-6" }`
- Deploy on Railway / Render (cheap and fast)
- Add API key auth for paid tiers

**Step 5.3 — Write and publish blog post**
- Title: "Why Lexile fails Indian students — and what we built instead"
- Publish on Medium + share on LinkedIn, Twitter/X, IndiaEdTech Slack
- Include FK vs ARI comparison with real NCERT examples

---

### Phase 6: AceQuest Internal Integration

**Step 6.1 — Update \****`readability-check`**\*\* skill**
- Replace or augment FK check with ARI score
- Report both: `{ "fk_grade": 5.8, "ari_score": 5.4, "verdict": "PASS" }`
- Verdict based on ARI (primary) with FK as sanity check

**Step 6.2 — Update \****`generate-passage`**\*\* skill**
- Add ARI target ranges per grade band
- Include ARI score in passage schema: `"ari_score": 5.4`

**Step 6.3 — Update the content pipeline plan**
- Replace "Flesch-Kincaid check" with "ARI check" in Stage 3 QA
- Update quality metric: `ari_score within target_grade ± 0.8`

**Step 6.4 — Student-facing label**
- Map ARI 1–10 → "Quest Level 1–10"
- Display on game pre-screen: "Quest Level 5 — recommended for Class 5-6 players"
- Doubles as a parent feature: "This game is Quest Level 6 — matches your child's class"

---

## Go-To-Market Strategy

### Target Customers (B2B)

| Segment | Who | Pain Point | ARI Value |
| --- | --- | --- | --- |
| **Ed-tech platforms** | BYJU'S, Vedantu, Toppr, Unacademy | Content difficulty mislabelled for Indian students | Drop-in API to score and label content correctly |
| **Publishers** | Oxford India, S Chand, Navneet | No automated readability check for new editions | Batch score manuscripts before printing |
| **Assessment companies** | EI ASSET, Pearson India | FK scores don't reflect Indian vocabulary | Replace FK with ARI in content QA pipeline |
| **NGOs / State boards** | Pratham (ASER), Akanksha | Need to measure reading level of field materials | Free open-source tier sufficient |

### Distribution

1. **Open-source first** — Python package on PyPI + GitHub. MIT licence. Builds trust and organic adoption.
2. **NCERT word frequency list as anchor asset** — Share as a dataset on HuggingFace. Drives discovery from ML community.
3. **Developer blog post** — "Why Lexile fails Indian students and what we built instead" — targets Indian ed-tech engineers.
4. **Paid pilots with 2 mid-size ed-tech companies** — Not BYJU'S first; approach funded Series A/B companies with content teams.
5. **Conference / research** — Submit a short paper or poster to IITB ICTD or IIM Ahmedabad EdTech conference for academic credibility.

### Pricing Model

| Tier | Price | Includes |
| --- | --- | --- |
| **Open Source** | Free | Python package, NCERT frequency list, model weights |
| **Starter API** | ₹999/month | 5,000 API calls/month, JSON response, email support |
| **Growth API** | ₹4,999/month | 50,000 calls/month, batch endpoint, priority support |
| **Enterprise** | Custom | Unlimited, SLA, on-premise deployment, custom training data |

Early adopters (first 10 companies): 6 months free on Growth tier in exchange for feedback and a case study.

---

## Data & Output Files

```
/ari/
├── data/
│   ├── corpus-labelled.jsonl          # All text segments with grade labels
│   ├── ncert-word-frequency.json      # Full word frequency list from NCERT corpus
│   ├── grade-vocab-lists.json         # Top-500 words per grade band
│   └── corpus-features.csv           # Feature matrix for model training
├── models/
│   ├── ari-model-v1.pkl              # Trained regression model
│   └── ari-calibration-table.json    # Known passages → ARI scores for reference
├── validation/
│   ├── validation-results.csv        # Test set predictions vs actual grades
│   └── teacher-validation-notes.md  # Expert reviewer feedback
└── README.md                         # How to use ARI
```

---

## Effort Estimate & Release Timeline

| Phase | Effort | Status |
| --- | --- | --- |
| Prerequisite: MD file validation | 0.5 day | ✅ Done |
| Phase 1: Corpus prep + frequency lists | 1 day | ✅ Done |
| Phase 2: Feature extraction | 0.5 day | ✅ Done |
| Phase 3: Model training (v1) | 1 day | ✅ Done (MAE gate not met) |
| **3.4–3.6: Corpus augmentation + retrain** | **1–2 days** | ✅ Done |
| Phase 4: Validation (internal + teachers) | 2–3 days | ⬜ Pending |
| FastAPI + Fly.io deployment | 0.5 day | ✅ Done |
| PyPI publish + HuggingFace | 0.5 day | ⬜ After MAE gate |
| Blog post + GitHub README | 0.5 day | ✅ Done |
| **FR-2: Feature breakdown in results** | **1 day** | ✅ Done |
| **FR-4: Grammar check** | **1–2 days** | ⬜ Planned |
| **FR-1: Hindi support** | **3–4 days** | ⬜ v2 roadmap |
| **FR-3: Progress tracking** | **3–4 days** | ⬜ v2 roadmap |
| Phase 6: AceQuest integration | 1 day | ⬜ After v1 release |

**Immediate priority:** Fix model MAE via StoryWeaver corpus augmentation → then FR-2 (feature breakdown) to address teacher trust feedback.

---

## Success Criteria

| Criterion | Target | Current Status |
| --- | --- | --- |
| Model MAE on test set | ≤ 0.8 grade levels | ❌ 1.65 — corpus augmentation complete, model saved |
| Within ±1 grade accuracy | 90% | ❌ 52% |
| Expert teacher agreement | ≥ 85% | ⬜ Not started |
| Coverage | Classes 1–10, all subjects | ✅ English done; Hindi planned (FR-1) |
| FK divergence cases | ARI outperforms FK ≥ 70% | ⬜ Not benchmarked |
| API live | Deployed | ✅ https://ari-acequest.fly.dev |
| Teacher feedback collection | Ongoing | ✅ SQLite feedback DB live |
| Detailed score breakdown | Per-feature explanation | ✅ FR-2 done |
| Grammar check | Flag grammatical errors | ✅ FR-4 completed |
| Progress tracking | Student/teacher history | ⬜ FR-3 planned (v2) |
| GitHub stars (3 months) | ≥ 100 | ⬜ PyPI not yet published |
| Paid API customers (6 months) | ≥ 3 | ⬜ Pre-launch |
| AceQuest integration | `readability-check` skill updated | ⬜ Phase 6 pending |

---

## Dependencies

| Dependency | Status |
| --- | --- |
| `/Books-MD/` corpus | ✅ 307 MD files converted (286 success + 21 retried) |
| Corpus labelled (JSONL) | ✅ 15,480 segments in `/ari/data/corpus-labelled.jsonl` |
| NCERT word frequency list | ✅ `/ari/data/ncert-word-frequency.json` |
| Grade vocab lists | ✅ `/ari/data/grade-vocab-lists.json` |
| Feature extractor | ✅ `ari/features.py` — 12 features |
| Corpus feature matrix | ✅ `/ari/data/corpus-features.csv` |
| Trained model (v1) | ✅ `ari/models/ari-model-v1.pkl` — MAE gate not yet met |
| FastAPI + Dockerfile | ✅ `ari/api/main.py` |
| Fly.io deployment | ✅ Live at https://ari-acequest.fly.dev |
| StoryWeaver augmentation data | ✅ Scrape complete, segments added, model retrained |
| 2 CBSE English teacher validators | ⬜ To be identified (needed for Phase 4) |
| LanguageTool setup (FR-4) | ⬜ Evaluate self-hosted vs API |
| Hindi NLP library (FR-1) | ⬜ Evaluate `indic-nlp-library` vs `stanza` |

---

## Chosen Tech Stack

> Full evaluation in [ari-tech-stack-evaluation.md](.//docs/decisions/drafts/ari-tech-stack-evaluation.md)

| Component | Tool | Why |
| --- | --- | --- |
| PDF → Markdown | **Mistral OCR API** | Best Hindi/Indian English quality, ~$3 for full corpus, one-time run |
| NLP tokenisation | **NLTK 3.9** | Lightweight, bundleable in PyPI package, Apache 2.0 |
| Syllable counting | **pyphen 0.17** | Pure Python, language-agnostic, fills NLTK's US-bias gap |
| ML training + inference | **scikit-learn 1.5** | 5 features × 5K–10K rows = classical regression; `.pkl` bundles in PyPI |
| Data manipulation | **pandas 2.2** | Standard for corpus feature matrix (CSV in/out) |
| API framework | **FastAPI 0.115** | Auto OpenAPI docs for B2B customers; Pydantic v2 validation built in |
| API server | **uvicorn 0.32** | ASGI server for FastAPI |
| Production hosting | **Fly.io (Mumbai \****`bom`**\*\*)** | Only PaaS with Mumbai region → <20ms Indian latency; free tier |
| Staging | **Render (free tier)** | Zero-cost staging; acceptable cold-starts for non-production |
| Package distribution | **PyPI** (`ari-india`) | Standard Python package manager |
| Dataset / model sharing | **HuggingFace Datasets** | ML community discoverability |

**Licences:** All Apache 2.0 / MIT / BSD-3. No GPL in production path.
**Hosting cost at launch:** $0–$2/month.
**One-time corpus cost:** ~$3 (Mistral OCR).

---

## Implementation Task Breakdown

### Pre-requisite: PDF to Markdown Conversion ✅ COMPLETE

- [x] **P0.1** Run Mistral OCR API pilot on 5 representative chapters (1 Math, 1 English, 1 Science, 2 different grades)
- [x] **P0.2** Pilot output validated — clean YAML frontmatter, readable prose, correct word counts
- [x] **P0.3** Full batch run on all 354 chapter PDFs via `scripts/pdf_to_markdown.py`
- [x] **P0.4** 307 MD files stored in `/Books-MD/{Subject}/Class-{N}/{Chapter}.md` with full frontmatter

**Result:** 307 chapters successfully converted. ~47 had transient Mistral 500 errors (retried — see `_conversion_log.json`). Corpus is sufficient for Phase 1 (need 500–1,000 segments per grade; 307 chapters across 10 grades easily provides this).

> **Note on remaining 47:** These were all transient API errors, not corrupt PDFs. Can be retried once before Phase 3. Corpus is not blocked — we have enough coverage across all grades.

---

### Phase 1: Corpus Preparation ✅ COMPLETE


---

### Phase 2: Feature Extraction ✅ COMPLETE

- [ ] **FR-3.2** Add optional `teacher_id` + `student_id` to feedback flow (cookie-based, no login required)
- [ ] **FR-3.3** `GET /teacher/{id}/history` — last 20 passages rated, per-student breakdown
- [ ] **FR-3.4** `GET /student/{id}/progress` — grade trend over time (are passages getting harder/easier?)
- [ ] **FR-3.5** Add "Next level" nudge: when student consistently scores ±0 from target grade for 3+ passages, suggest bumping target grade by 1
- [ ] **FR-3.6** Simple history view in web UI — "You've checked 5 passages. Class 4 students are ready for Grade 5 material."
- [ ] **FR-3.7** Privacy: all IDs are anonymous tokens; no PII collected; opt-in history via local storage or cookie
**Problem:** Teachers want to know not just *difficulty level* but also *grammatical correctness* — especially for passages sourced from non-standard materials.
- [x] **1.1** `corpus_builder.py` — prose extraction from `/Books-MD/` → `/ari/data/corpus-labelled.jsonl` (15,480 segments across Grades 1–10)
- [x] **1.2** `build_frequency_list.py` → `/ari/data/ncert-word-frequency.json`
- [x] **1.3** `build_vocab_lists.py` → `grade-vocab-lists.json`, `grade-band-vocab-lists.json`, `grade-subject-vocab-lists.json`
- [x] StoryWeaver augmentation pipeline — `fetch_storyweaver.py` + `build_storyweaver_corpus.py`
**Problem:** Tool is currently stateless per-session. No way to track whether a student is improving, or guide teachers to progressively harder passages.
---

### Phase 3: Model Training ✅ COMPLETE (MAE gate NOT yet met)

- [ ] **3.1** `train_model.py` — GradientBoosting vs Ridge; GradientBoosting selected
- [x] **3.2** Model serialised → `ari/models/ari-model-v1.pkl`
- [x] **3.3** Model card → `ari/models/model-card.json`

**Current model metrics (2026-02-21):**

| Metric | Value | Target | Status |
| --- | --- | --- | --- |
| Test MAE | 1.65 | ≤ 0.8 | ❌ Not met |
| Test R² | 0.40 | — | — |
| Within ±1 grade | 52% | 90% | ❌ Not met |

> **Root cause:** Lower grades (1–4) have very short prose fragments → weak grade signal. Added StoryWeaver augmentation which improved elementary grades but shifted overall distributions.

**Next steps to improve model:**
- [x] **3.4** Augment corpus with StoryWeaver graded stories (already scraped in `ari/augmentation/storyweaver/`)
- [x] **3.5** Re-train with augmented corpus
- [ ] **3.6** Try ordinal regression or multi-label classification as alternative model type

---

### Phase 4: Validation ⬜ PENDING (blocked on MAE gate)

- [ ] **4.1** Internal validation on 20 held-out chapters → `/ari/validation/validation-results.csv`
- [ ] **4.2** Cross-validate ARI vs FK on 50 passages — document divergence cases for blog post
- [ ] **4.3** Expert validation with 2 CBSE English teachers (target: ≥ 85% agreement)

---

### Phase 5: FastAPI + Deployment ✅ COMPLETE (v1 live)

- [x] **5.1** `ari/api/main.py` — FastAPI with `POST /score`, `POST /feedback`, `POST /nps`, `GET /health`
- [x] **5.2** Cloudflare Turnstile CAPTCHA on feedback endpoint
- [x] **5.3** `slowapi` rate limiting (10 req/min score, 5 req/min feedback)
- [x] **5.4** SQLite feedback DB (`feedback.db`) — stores teacher ratings for model retraining
- [x] **5.5** Deployed to Fly.io → **https://ari-acequest.fly.dev**
- [ ] **5.6** PyPI publish (`ari-india` package) — deferred until MAE gate is met
- [ ] **5.7** HuggingFace Datasets upload (`acequest/ncert-word-frequency`)

---

### Phase 6: AceQuest Internal Integration ⬜ PENDING

- [ ] **6.1** Update `skills/content-creators/readability-check.md` — add ARI as primary scorer
- [ ] **6.2** Update `skills/content-creators/generate-passage.md` — add `ari_score` to output schema
- [ ] **6.3** Update `plans/content-creation-pipeline.md` Stage 3 QA — replace FK with ARI

**Problem:** Current result only shows `Grade X–Y`. Teacher cannot understand *why* that grade was assigned or verify the scoring logic.
---

## User Feedback — Feature Requests (captured 2026-02-21)

Four items raised by early users. Prioritised below.

### FR-1: Regional Language Support 🔴 HIGH PRIORITY

> "Is it only for English? Local language is required as bulk of Indians should be literate at least in their mother tongue."

**Problem:** Tool only supports English passages. Hindi, Tamil, Telugu, Kannada, Marathi etc. are the primary medium of instruction for most Indian students.

**Plan:**
- [ ] **FR-1.1** Define scope: start with **Hindi** (largest user base, NCERT Hindi corpus already available in `/Books-MD/`)
- [ ] **FR-1.2** Audit `/Books-MD/` for Hindi chapter MD files — check if OCR quality is adequate for prose extraction
- [ ] **FR-1.3** Build Hindi feature extractor:
  - Tokenisation: use `indic-nlp-library` or `stanza` with Hindi model
  - Syllable counting: Hindi syllabification is vowel-based — write custom rule or use `indic-nlp-library`
  - Word frequency: build NCERT Hindi word frequency list from Hindi chapter corpus
- [ ] **FR-1.4** Train separate Hindi ARI model (same architecture, Hindi corpus)
- [ ] **FR-1.5** Add `language` field to `POST /score` and `POST /feedback` requests (`"en"` | `"hi"`)
- [ ] **FR-1.6** Update web UI: add language selector (English / Hindi); show script-appropriate fonts
- [ ] **FR-1.7** After Hindi: evaluate Marathi, Tamil based on demand signals

**Deferred:** Other regional languages to v3 after Hindi is validated.


---

### FR-2: Detailed Feature Breakdown in Results 🔴 HIGH PRIORITY

> "Your rating should include the parameters you assessed — sentence length, word complexity (highlight the words that exceed complexity), vocab richness, syllable density."


**Plan:**
- [x] **FR-2.1** Update `POST /score` response to include `features` breakdown:
```json
  {
    "grade_low": 3, "grade_mid": 4, "grade_high": 5,
    "label": "Grade 3–5",
    "features": {
      "avg_sentence_length": 12.4,
      "word_complexity": "moderate",
      "vocab_richness": "high",
      "syllable_density": 1.8,
      "pct_rare_words": 14.2,
      "assessment": "Sentence length is appropriate for Grade 4. Contains some challenging vocabulary (14% rare words). 💡 Suggestion: Substitute the highlighted tricky words below for simpler alternatives."
    },
    "complex_words": ["photosynthesis", "chlorophyll", "ecosystem"]
  }
```
- [x] **FR-2.2** Add dual `complex_words` lists:
  - Base list calculated against the model's predicted grade.
  - Secondary `teacher_complex_words` calculated against the teacher's selected rating via `/feedback`.
- [x] **FR-2.3** Add natural-language `assessment` string explaining the score in teacher-friendly terms (template-based, not LLM)
- [x] **FR-2.4** Update web UI (`app.js` / `index.html`) to display:
  - Feature bar chart or mini-scorecard showing each dimension
  - Highlighted complex words inline in the passage text (or listed below)
  - "Why this grade?" expandable section

---

### FR-3: Teacher & Student History / Progress Tracking 🟡 MEDIUM PRIORITY

> "You need to maintain history of the student and teacher as they work so that your system can track progress or lack of it, and push the teacher to select the next passage level."


**Plan:**
- [ ] **FR-3.1** Design data model for teacher/student sessions:
  - `Teacher` (anonymous ID, board, grade taught)
  - `Student` (anonymous ID, linked to teacher, current target grade)
  - `Session` (student, passage, teacher_grade, ari_grade, timestamp)

**Note:** This is a significant scope expansion — builds toward a mini "reading progress tracker" product. Keep v1 anonymous/stateless; introduce history as opt-in in v2.

---

### FR-4: Grammar and Sentence Structure Check 🟡 MEDIUM PRIORITY

> "Does not check for grammar and wrong sentence structures."


**Plan:**
- [ ] **FR-4.1** Evaluate grammar checking options:
  - `language_tool_python` (LanguageTool — open source, Java-based, good for Indian English)
  - `gingerit` (lightweight but cloud-based)
  - Preference: LanguageTool — self-hosted, supports Indian English quirks better than Grammarly API
- [ ] **FR-4.2** Add `POST /grammar` endpoint (separate from `/score` to keep scoring fast):
```json
  { "text": "...", "language": "en" }
  → { "errors": [{ "offset": 12, "length": 5, "message": "...", "rule": "GRAMMAR" }], "error_count": 3 }
```
- [ ] **FR-4.3** Add `sentence_structure_issues` to the score response — flag very long or very short outlier sentences
- [ ] **FR-4.4** Update web UI: optional "Check grammar" toggle; show error highlights inline
- [ ] **FR-4.5** Indian English consideration: LanguageTool has known false positives on Indian English patterns (e.g. "she is having a book"). Build a suppression list for common Indian English constructions that are grammatically valid in context.

---

## Future Extensions (v2+)

- **Parse depth feature** — spaCy dependency parser for syntactic complexity
- **Concept density** — domain-specific terms per 100 words using chapter concept JSON
- **Subject-specific models** — separate models for Math vs English vs Science
- **Batch API endpoint** — score entire chapters or manuscripts in one request
- **HuggingFace model card** — publish model weights for ML community discoverability
- **Hindi ARI** — see FR-1 above (promoted to active roadmap)
- **Student progress tracking** — see FR-3 above (promoted to active roadmap)

---

## Related Documents

- [content-creation-pipeline.md](./content-creation-pipeline.md) — where ARI integrates (Stage 3 QA)
- [readability-check.md](./../skills/content-creators/readability-check.md) — skill to be updated with ARI
- [generate-passage.md](./../skills/content-creators/generate-passage.md) — passages will be scored by ARI
- [validate-markdown.md](./../skills/content-creators/validate-markdown.md) — prerequisite MD validation skill
