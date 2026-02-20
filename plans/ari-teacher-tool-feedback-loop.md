---
planStatus:
  planId: plan-ari-teacher-tool
  title: ARI Teacher Tool — Free Public Access + Feedback Loop
  status: draft
  planType: feature
  priority: high
  owner: raghavrohatgi
  stakeholders: []
  tags:
    - ari
    - teacher
    - feedback
    - retraining
    - api
  created: "2026-02-20"
  updated: "2026-02-20T06:00:00.000Z"
  progress: 0
---
# ARI Teacher Tool — Free Public Access + Feedback Loop

## UI Mockup

![ARI Teacher Tool Mockup](screenshot.png){mockup:nimbalyst-local/mockups/ari-teacher-tool.mockup.html}{960x700}

*Mockup shows both UI states side by side. Left: teacher rates first (before seeing ARI). Right: ARI result revealed after teacher submits.*

---

## Objective

Make the ARI readability model freely available to Indian teachers via a simple web tool, while collecting the teacher-submitted passages and their ratings to:
1. Measure agreement between ARI predictions and teacher judgement
2. Identify systematic bias and retrain the model with real-world signal

---

## What We're Building

Three tightly coupled components:

### 1. ARI API (FastAPI on Fly.io)
A lightweight REST API that wraps the trained `ari-model-v1.pkl`.

**Endpoint: \****`POST /score`** (rate-limited: 10 req/min/IP)
```json
Request:  { "text": "...", "subject": "English" }
Response: { "grade_low": 3, "grade_mid": 4, "grade_high": 5, "label": "Grade 3–5" }
```
Returns a **range**, not a point estimate — more honest, less contentious for teachers.

**Endpoint: \****`POST /feedback`** (rate-limited: 5 req/min/IP)
```json
Request:  {
  "text": "...",
  "subject": "English",
  "ari_grade_mid": 4,
  "teacher_grade": 3,
  "teacher_board": "CBSE",
  "reason": "optional free text"
}
Response: { "ok": true }
```

`/stats` endpoint **removed** — feedback data kept internal only.

### 2. Teacher Web Tool (Static HTML + vanilla JS)
A single-page tool hosted on GitHub Pages or Fly.io — no login required.

**Flow:**
1. Teacher pastes a passage (textarea)
2. Selects subject (English / Maths / Science / EVS)
3. Clicks "Check Reading Level"
4. **Teacher rates first**: "What grade would YOU assign?" → 1–10 pill buttons
5. Teacher submits their rating
6. ARI result revealed: **"Grade 3–5"** (range, not point) with confidence bar
7. If teacher grade is outside the ARI range → optional "Why do you disagree?" text box appears
8. Data stored internally in feedback DB

**Key UX principles:**
- No signup, no email, no friction
- Works on mobile (teachers use phones)
- Hindi UI option (toggle) for non-English-comfortable teachers
- Shows ARI grade AFTER teacher picks (to avoid anchoring bias)

### 3. Feedback Database + Retraining Pipeline

**Storage:** SQLite (Fly.io volume) → exportable CSV

**Schema:**
```sql
CREATE TABLE feedback (
  id          TEXT PRIMARY KEY,
  created_at  DATETIME,
  text        TEXT,         -- the passage
  text_hash   TEXT,         -- sha256 for dedup
  ari_grade   REAL,         -- model prediction
  teacher_grade INTEGER,    -- teacher's rating (1-10)
  grade_diff  REAL,         -- teacher_grade - ari_grade
  teacher_yoe INTEGER,      -- years of experience
  teacher_board TEXT,       -- CBSE / ICSE / State
  teacher_subject TEXT,
  teacher_state TEXT,
  reason      TEXT,         -- optional free text
  source      TEXT          -- "web_tool" / "acequest_app"
);
```

**Retraining trigger:** When `feedback` table has ≥200 new rows since last retrain, run:
1. Export agreed passages (|grade_diff| ≤ 1) as new corpus entries with teacher_grade label
2. Append to `corpus-labelled.jsonl`
3. Re-run `extract_corpus_features.py` + `train_model.py`
4. If new MAE < old MAE: promote new model
5. Log delta to `model-card.json`

---

## Agreement Analytics

Track these metrics per batch of 50+ feedbacks:

| Metric | Formula | Target |
| --- | --- | --- |
| Exact agreement | teacher == round(ari) | >30% |
| Within-1 agreement | \ | teacher - ari\ | ≤ 1 | >60% |
| Bias by grade | mean(teacher - ari) per grade | < ±0.5 |
| Expert vs novice gap | MAE difference YOE > 5 vs < 5 | < 0.3 |

If `mean(teacher - ari) > 0.5` for a grade → ARI is under-predicting for that grade → apply calibration offset.

---

## Deployment Stack

| Component | Technology | Cost |
| --- | --- | --- |
| API | FastAPI + joblib (Python) | Fly.io free tier (256MB RAM) |
| Web Tool | Static HTML/CSS/JS | Fly.io or GitHub Pages (free) |
| Database | SQLite on Fly.io volume | Free (included) |
| Domain | acequest.in/ari or ari.acequest.in | ₹800/yr |
| Analytics dashboard | Observable notebook or Streamlit | Free |

Total cost: ~₹800/year (just domain).

---

## Data Privacy

- No PII collected — no names, no emails, no school names
- Passages are stored (needed for retraining) — state this clearly in UI: "We store the text you paste to improve ARI"
- Teachers from the same school submitting same passage: deduplicated by `text_hash`
- DPDPA 2023 compliant: no sensitive personal data, no children's data

---

## Implementation Steps

### Phase 5A — API (Week 1)
- [ ] Create `ari/api/main.py` (FastAPI app)
- [ ] `POST /score` — loads model, returns prediction + features
- [ ] `POST /feedback` — writes to SQLite
- [ ] `GET /stats` — aggregate counts
- [ ] Dockerfile + `fly.toml`
- [ ] Deploy to Fly.io Mumbai region

### Phase 5B — Web Tool (Week 1-2)
- [ ] `ari/web/index.html` — single file, no build step
- [ ] Textarea + submit button
- [ ] Show ARI grade after teacher picks theirs (prevents anchoring)
- [ ] Mobile-responsive CSS
- [ ] Deploy alongside API

### Phase 5C — Analytics (Week 2)
- [ ] `ari/scripts/analyze_feedback.py`
  - Agreement rate per grade
  - Bias direction per grade
  - Per-subject breakdown
  - Export to CSV for Streamlit/Observable
- [ ] Streamlit dashboard at `/dashboard` (password-protected for internal use)

### Phase 5D — Retraining Loop (Week 3)
- [ ] `ari/scripts/retrain_from_feedback.py`
  - Filter high-confidence agreed passages (|diff| ≤ 1, YOE ≥ 3)
  - Append to corpus
  - Trigger full retrain pipeline
  - Compare MAE before/after, promote if better
- [ ] Cron job or manual trigger (Fly.io scheduled machine)

---

## What Teachers Bring In vs ARI

The key research question: **Do teachers agree with ARI, or do they see something ARI misses?**

Expected patterns:
- **Poetry / songs**: ARI over-predicts difficulty (short lines, simple words but high FK from syllables)
- **Dialogue-heavy text**: ARI under-predicts (conversational register, easy to read but many sentences)
- **Domain jargon**: ARI correctly flags as hard; teachers may disagree if students know the domain

Collecting these disagreements by subject and grade gives us a systematic map of where ARI is wrong — this directly drives the next feature engineering cycle.

---

## Success Metrics

| Metric | Target (Month 1) | Target (Month 3) |
| --- | --- | --- |
| Feedback submissions | 100 | 500 |
| Unique teachers | 20 | 100 |
| Agreement rate (within 1) | Baseline measurement | Improvement after retrain |
| New model MAE (after retrain) | — | < 1.5 overall, < 2.0 for Grades 1-3 |

---

## Resolved Decisions

| Question | Decision |
| --- | --- |
| Point estimate vs grade range? | **Show range** (e.g., "Grade 3–5") — more honest about model uncertainty, less alienating when teachers disagree |
| Subject selector? | **Yes** — English / Maths / Science / EVS / Hindi / Other. Improves rare-word signal and helps us analyse disagreements by domain |
| Share feedback data publicly? | **No** — keep internal. Use for retraining only |
| CAPTCHA? | **Yes** — Cloudflare Turnstile on `/feedback` submission only. Free, mobile-friendly, no image puzzles |

---

## Abuse Protection & DoS Mitigation

Since the tool is open (no login), we need lightweight protection:

### Rate Limiting (Primary defence)
- Per-IP: max **10 requests/minute** to `/score`, **5 submissions/minute** to `/feedback`
- Implemented via `slowapi` (FastAPI middleware, 5 lines of code)
- Returns HTTP 429 with `Retry-After` header

### Request Validation
- Max passage length: **5,000 characters** (hard cap — rejects bulk automation)
- Min passage length: **20 characters** (rejects empty/junk submissions)
- `Content-Type: application/json` required (blocks naive scanners)

### DoS / Cost Protection
- Fly.io free tier auto-sleeps after 5 min idle — attacker wakes it but can't keep it overwhelmed for long
- Fly.io has built-in DDoS scrubbing at network layer (included free)
- `/score` is stateless and fast (~50ms) — not expensive enough to be a meaningful DoS target
- `/feedback` writes to SQLite — cap DB size at 500MB, auto-reject above that

### Feedback Quality Guard
- Minimum 20 words in submitted passage before feedback is stored
- Duplicate detection: `sha256(text)` — same passage submitted twice by same IP within 1 hour → silently ignored
- Teacher grade must be 1–10 integer — reject anything outside that

### CAPTCHA
- **Where**: On `/feedback` submission only (not on `/score`) — scoring is read-only and cheap; feedback writes to DB
- **Which**: [Cloudflare Turnstile](https://developers.cloudflare.com/turnstile/) — **free**, privacy-friendly, no image puzzles, works well on mobile
  - Renders as a simple checkbox "I am human" or auto-solves invisibly for real browsers
  - Far less friction than reCAPTCHA v2 on phones
- **Why not on /score**: Teachers paste and score freely; CAPTCHA only appears when they submit a rating
- Turnstile token verified server-side via `POST ``https://challenges.cloudflare.com/turnstile/v0/siteverify`

### Monitoring
- Log all 429 responses with IP + timestamp to a `rate_limit_log` table
- Weekly cron: flag IPs with >500 blocked requests → add to deny list in `fly.toml`
- Alert (Fly.io email) if feedback table grows >10,000 rows in a single day (anomalous)
