# AceQuest — ARI for Indian Education

**Automated Readability Index (ARI) calibrated for CBSE/ICSE grades 1–10.**

This repository contains:
- **NCERT textbook corpus** (Books-MD/) — converted from PDF to Markdown
- **ARI readability model** — GradientBoosting regressor with 12 linguistic features
- **Teacher feedback tool** — free web app for collecting teacher ratings
- **API** — FastAPI service for scoring passages

---

## Project Structure

```
AceQuest/
├── Books-MD/              # NCERT textbooks (Markdown, grades 1-10)
├── ari/
│   ├── features.py        # Feature extraction (FK grade, TTR, syllables, etc.)
│   ├── models/            # Trained model (ari-model-v1.pkl)
│   ├── data/              # Corpus and feature CSVs
│   ├── scripts/           # Training and corpus building scripts
│   ├── api/               # FastAPI app + SQLite feedback DB
│   ├── web/               # Teacher web tool (static HTML)
│   └── augmentation/      # StoryWeaver stories (CC-BY licensed)
└── plans/                 # Feature plans and roadmaps
```

---

## Current Model Performance

| Metric | Value |
|--------|-------|
| Overall MAE | 1.628 |
| Within ±1 grade | 37.3% |
| R² | 0.436 |

### Per-grade MAE:
- Grade 1: 2.414
- Grade 2: 2.150
- Grade 3: 1.899
- Grade 7: 0.714 ✓
- Grade 8: 1.027 ✓

---

## Quick Start

### Train the model locally
```bash
python3 ari/scripts/corpus_builder.py
python3 ari/scripts/extract_corpus_features.py
python3 ari/scripts/train_model.py
```

### Run the API locally
```bash
pip install -r ari/api/requirements.txt
export ARI_DEV_MODE=true
uvicorn ari.api.main:app --reload --port 8080
```

### Deploy to Fly.io
```bash
fly deploy --config ari/api/fly.toml
fly secrets set TURNSTILE_SECRET=<your_secret>
```

---

## License

- **Code**: MIT
- **Books-MD corpus**: NCERT textbooks are public domain in India
- **StoryWeaver stories**: CC-BY 4.0 (attributions in YAML frontmatter)

---

Built with ❤️ for Indian education.
