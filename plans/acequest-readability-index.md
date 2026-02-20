---
planStatus:
  planId: plan-acequest-readability-index
  title: AceQuest Readability Index (ARI)
  status: active
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
  updated: "2026-02-18T00:00:00.000Z"
  progress: 15
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

**Step 6.1 — Update `readability-check` skill**
- Replace or augment FK check with ARI score
- Report both: `{ "fk_grade": 5.8, "ari_score": 5.4, "verdict": "PASS" }`
- Verdict based on ARI (primary) with FK as sanity check

**Step 6.2 — Update `generate-passage` skill**
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

| Phase | Effort | Week |
| --- | --- | --- |
| Prerequisite: MD file validation (pilot 5 chapters) | 0.5 day | Week 1 |
| Phase 1: Corpus prep + word frequency list | 1 day | Week 1 |
| Phase 2: Feature extraction pipeline | 0.5 day | Week 1 |
| Phase 3: Model training + calibration | 1 day | Week 2 |
| Phase 4: Validation (internal + 2 teachers) | 2–3 days | Week 2–3 |
| Python package + PyPI publish | 0.5 day | Week 3 |
| FastAPI wrapper + deployment | 0.5 day | Week 3 |
| Blog post + GitHub README | 0.5 day | Week 3 |
| **Total** | **~6–7 days** | **3 weeks** |

**Week 3 = v1 public release.**

---

## Success Criteria

| Criterion | Target |
| --- | --- |
| Model MAE on test set | ≤ 0.8 grade levels |
| Expert teacher agreement | ≥ 85% of passages rated "appropriate" for ARI-assigned level |
| Coverage | Works reliably for Classes 1–10, all three subjects |
| FK divergence cases | ARI outperforms FK on ≥ 70% of cases where they disagree (validated by teachers) |
| GitHub stars (3 months) | ≥ 100 |
| Paid API customers (6 months) | ≥ 3 paying companies |
| AceQuest integration | `readability-check` skill updated and returning ARI scores |

---

## Dependencies

| Dependency | Status |
| --- | --- |
| `/Books-MD/` corpus complete | ✅ **307 MD files converted** (286 success + 21 retried) |
| MD file validation | ⬜ Next immediate step — validate YAML frontmatter + prose quality |
| Python NLP environment | ⬜ Need: `nltk`, `pyphen`, `scikit-learn`, `pandas` |
| 2 CBSE English teacher validators | ⬜ To be identified (needed for Phase 4) |

---

## Chosen Tech Stack

> Full evaluation in [`/docs/decisions/drafts/ari-tech-stack-evaluation.md`](/docs/decisions/drafts/ari-tech-stack-evaluation.md)

| Component | Tool | Why |
| --- | --- | --- |
| PDF → Markdown | **Mistral OCR API** | Best Hindi/Indian English quality, ~$3 for full corpus, one-time run |
| NLP tokenisation | **NLTK 3.9** | Lightweight, bundleable in PyPI package, Apache 2.0 |
| Syllable counting | **pyphen 0.17** | Pure Python, language-agnostic, fills NLTK's US-bias gap |
| ML training + inference | **scikit-learn 1.5** | 5 features × 5K–10K rows = classical regression; `.pkl` bundles in PyPI |
| Data manipulation | **pandas 2.2** | Standard for corpus feature matrix (CSV in/out) |
| API framework | **FastAPI 0.115** | Auto OpenAPI docs for B2B customers; Pydantic v2 validation built in |
| API server | **uvicorn 0.32** | ASGI server for FastAPI |
| Production hosting | **Fly.io (Mumbai `bom`)** | Only PaaS with Mumbai region → <20ms Indian latency; free tier |
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

### Phase 1: Corpus Preparation ← **START HERE**

- [ ] **1.1** Write `corpus_builder.py` script:
  - Walk `/Books-MD/` directory tree
  - For each chapter MD: strip frontmatter, headings, exercise blocks (lines starting with Q., question numbers, `**Exercise**`)
  - Extract prose paragraphs only (≥20 words, not inside LaTeX blocks)
  - Label each segment: `{"text": "...", "grade": 6, "subject": "science"}`
  - Output: `/ari/data/corpus-labelled.jsonl`
  - Target: 500–1,000 labelled segments per grade level (Grades 1–10)

- [ ] **1.2** Write `build_frequency_list.py`:
  - Pool all prose text across all grades
  - Tokenise with `nltk.word_tokenize`, lowercase, remove punctuation
  - Count frequency of every word → sorted ranked list
  - Output: `/ari/data/ncert-word-frequency.json` — `[{"word": "magnet", "frequency": 234, "rank": 1820}, ...]`

- [ ] **1.3** Write `build_vocab_lists.py`:
  - Run frequency analysis separately for grade bands: 1-3, 4-6, 7-10
  - Extract top 500 words per band = "familiar vocabulary"
  - Output: `/ari/data/grade-vocab-lists.json` — `{"1-3": ["the", "a", ...], "4-6": [...], "7-10": [...]}`

**Validation:** Spot-check 3 grade levels — top-500 words for Grade 1 should be basic sight words; Grade 9-10 should include subject terms.

---

### Phase 2: Feature Extraction

- [ ] **2.1** Write `ari/features.py` — `FeatureExtractor` class:

  ```python
  class FeatureExtractor:
      def extract(self, text: str, grade_band: str) -> dict:
          # Returns dict with all 5 features
  ```

  Features to compute:
  - `mean_word_frequency_rank` — avg NCERT corpus rank of content words
  - `mean_sentence_length` — avg tokens per sentence (`sent_tokenize` + `word_tokenize`)
  - `type_token_ratio` — unique words / total words
  - `avg_syllables_per_word` — using `pyphen` (language `en_GB` as closest to Indian English)
  - `pct_rare_words` — % words not in top-500 for the given grade band

- [ ] **2.2** Write `extract_corpus_features.py` script:
  - Load `corpus-labelled.jsonl`
  - For each segment: run `FeatureExtractor.extract(text, grade_to_band(grade))`
  - Output: `/ari/data/corpus-features.csv` (columns: `grade`, + 5 feature columns)

- [ ] **2.3** Sanity check: plot feature distributions per grade (boxplots) — confirm monotonic trend (features should generally increase with grade level)

---

### Phase 3: Model Training

- [ ] **3.1** Write `train_model.py`:
  - Load `corpus-features.csv`
  - 80/20 train/test split (stratified by grade)
  - Train: `Ridge(alpha=1.0)` and `GradientBoostingRegressor(n_estimators=100)`
  - 5-fold cross-validation on train set
  - Evaluate both on test set: compute MAE, R², per-grade error breakdown
  - Select model with lower MAE

- [ ] **3.2** Calibration check:
  - Take 10 known-grade NCERT passages (held out from training)
  - Verify: Class 6 passage scores 5.5–6.5 on ARI scale
  - If consistently off: apply `min-max calibration` to map raw output → 1–10 range
  - Save calibration parameters inside model pipeline

- [ ] **3.3** Serialise winning model:
  - `joblib.dump(pipeline, "models/ari-model-v1.pkl")`
  - Record: model type, MAE, R², training date, corpus size → `models/model-card.json`

**Success gate:** MAE ≤ 0.8 on test set. If not achieved, diagnose corpus (likely too few segments for some grades) before trying a more complex model.

---

### Phase 4: Validation

- [ ] **4.1** Internal validation:
  - Run ARI on 20 held-out chapters not used in training
  - Target: 90% of segments within ±1 of true grade
  - Document failures in `/ari/validation/validation-results.csv`

- [ ] **4.2** Cross-validate against FK:
  - Run both ARI and FK (current `readability-check` skill) on same 50 passages
  - Document divergence cases — especially where FK is wrong for Indian content
  - These divergence examples become the centrepiece of the blog post

- [ ] **4.3** Expert validation (2 CBSE English teachers):
  - Share 20 test passages with ARI scores
  - Question: "Is this difficulty level appropriate for Grade X students?"
  - Adjust calibration if agreement < 85%

---

### Phase 5: Package & API

- [ ] **5.1** Package structure — create `ari-india/` repo:
  ```
  ari-india/
  ├── ari/
  │   ├── __init__.py          # exports: score(), ARI_VERSION
  │   ├── scorer.py            # score(text, grade_band) → ARIResult
  │   ├── features.py          # FeatureExtractor class
  │   ├── model.py             # load_model(), predict()
  │   └── data/
  │       ├── ncert-word-frequency.json
  │       └── grade-vocab-lists.json
  ├── models/
  │   └── ari-model-v1.pkl
  ├── tests/
  │   ├── test_features.py
  │   ├── test_scorer.py
  │   └── fixtures/            # 10 reference passages with known grades
  ├── pyproject.toml           # PEP 517 build; dependencies: nltk, pyphen, scikit-learn, pandas
  ├── README.md
  └── LICENSE                  # MIT
  ```

- [ ] **5.2** `scorer.py` public interface:
  ```python
  from dataclasses import dataclass

  @dataclass
  class ARIResult:
      score: float           # 1.0–10.0
      label: str             # "Suitable for Class 5 (range: 5–6)"
      quest_level: int       # 1–10 (for AceQuest internal use)
      grade_band: str        # "4-6"
      features: dict         # raw feature values (for debugging)

  def score(text: str, grade_band: str = "4-6") -> ARIResult:
      ...
  ```

- [ ] **5.3** FastAPI wrapper — `ari-api/main.py`:
  ```
  POST /score
  Body: { "text": "...", "grade_band": "4-6" }
  Response: { "score": 5.3, "label": "...", "quest_level": 5, "features": {...} }

  GET /health → { "status": "ok", "model_version": "v1" }
  GET /docs   → auto OpenAPI docs (FastAPI built-in)
  ```
  - API key auth via `X-API-Key` header (simple dict lookup from env var for v1)
  - Rate limiting: `slowapi` library (100 req/min per API key)
  - Dockerfile: `python:3.12-slim`, no GPU required

- [ ] **5.4** Publish:
  - [ ] `git init` + push to GitHub (MIT licence, public)
  - [ ] `python -m build` + `twine upload` → PyPI (`ari-india`)
  - [ ] Upload `ncert-word-frequency.json` to HuggingFace Datasets (`acequest/ncert-word-frequency`)
  - [ ] Deploy API to Fly.io Mumbai: `flyctl launch` → `flyctl deploy`

---

### Phase 6: AceQuest Internal Integration

- [ ] **6.1** Update `skills/content-creators/readability-check.md`:
  - Add ARI as primary scorer; FK as secondary/sanity check
  - New output schema: `{ "fk_grade": 5.8, "ari_score": 5.4, "primary": "ari", "verdict": "PASS" }`

- [ ] **6.2** Update `skills/content-creators/generate-passage.md`:
  - Add `"ari_score": 5.4` to passage output schema
  - Add ARI target ranges per grade band (align to ARI calibration table)

- [ ] **6.3** Update `plans/content-creation-pipeline.md` Stage 3 QA:
  - Replace "FK check" → "ARI check (primary) + FK (sanity)"
  - Update quality gate: `ari_score within target_grade ± 0.8`

---

## Future Extensions (v2)

- **Parse depth feature** using a lightweight dependency parser (spaCy) for syntactic complexity
- **Concept density** — count domain-specific terms per 100 words using the chapter concept JSON
- **Multi-language ARI** — extend to Hindi passages once Hindi NCERT corpus is ingested
- **Subject-specific models** — separate models for Math (formula-heavy) vs English vs Science
- **Web dashboard** — paste text, get ARI score instantly (freemium lead magnet)
- **Batch API endpoint** — score entire chapters or manuscripts in one request
- **HuggingFace model card** — publish model weights for ML community discoverability

---

## Related Documents

- [content-creation-pipeline.md](./content-creation-pipeline.md) — where ARI integrates (Stage 3 QA)
- [readability-check.md](./../skills/content-creators/readability-check.md) — skill to be updated with ARI
- [generate-passage.md](./../skills/content-creators/generate-passage.md) — passages will be scored by ARI
- [validate-markdown.md](./../skills/content-creators/validate-markdown.md) — prerequisite MD validation skill
