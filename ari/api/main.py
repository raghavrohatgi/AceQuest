"""
ARI API — FastAPI application.

Endpoints:
  POST /score     — Score a passage, return grade range
  POST /feedback  — Store teacher rating (Turnstile CAPTCHA required)

Rate limiting via slowapi (per-IP).
"""

import os
import sys
from pathlib import Path

import httpx
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# --- Paths ---
ROOT = Path(__file__).parent.parent.parent  # AceQuest/
sys.path.insert(0, str(ROOT))

from ari.features import FeatureExtractor
from ari.api.db import (
    db_size_ok,
    feedback_count,
    init_db,
    insert_feedback,
    is_duplicate,
)

# --- Model ---
MODEL_PATH = Path(__file__).parent.parent / "models" / "ari-model-v1.pkl"
_pipeline = None  # Loaded on startup

FEATURE_COLS = [
    "mean_word_frequency_rank",
    "mean_sentence_length",
    "type_token_ratio",
    "avg_syllables_per_word",
    "pct_rare_words",
    "mean_log_freq_rank",
    "lexical_density",
    "flesch_kincaid_grade",
    "gunning_fog",
    "sentence_length_variance",
    "subordinate_clause_ratio",
    "long_word_ratio",
]

_fe = FeatureExtractor()

# --- Cloudflare Turnstile ---
TURNSTILE_SECRET = os.environ.get("TURNSTILE_SECRET", "")
TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

# In development mode, skip Turnstile verification
DEV_MODE = os.environ.get("ARI_DEV_MODE", "false").lower() == "true"

# --- Rate limiter ---
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="ARI — Indian Reading Level API",
    description="Automated Readability Index calibrated for CBSE/ICSE grades 1–10",
    version="1.0.0",
    docs_url="/docs" if DEV_MODE else None,  # hide Swagger in production
    redoc_url=None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to acequest.in domain after launch
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


@app.on_event("startup")
def startup():
    global _pipeline
    print("[ARI] Loading model from disk...")
    _pipeline = joblib.load(MODEL_PATH)
    print("[ARI] Model loaded successfully")
    init_db()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _predict_range(text: str, subject: str) -> dict:
    """Run the ARI model and return a grade range."""
    features = _fe.extract(text, grade=5, subject=subject)  # grade=5 neutral baseline
    X = np.array([[features[col] for col in FEATURE_COLS]])
    mid_raw = float(np.clip(_pipeline.predict(X)[0], 1.0, 10.0))

    mid = round(mid_raw)
    low = max(1, mid - 1)
    high = min(10, mid + 1)

    return {
        "grade_low": low,
        "grade_mid": mid,
        "grade_high": high,
        "label": f"Grade {low}–{high}" if low != high else f"Grade {mid}",
    }


async def _verify_turnstile(token: str, ip: str) -> bool:
    """Verify Cloudflare Turnstile token. Returns True if valid."""
    if DEV_MODE:
        return True
    if not TURNSTILE_SECRET:
        return False
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.post(
            TURNSTILE_VERIFY_URL,
            data={"secret": TURNSTILE_SECRET, "response": token, "remoteip": ip},
        )
    data = resp.json()
    return data.get("success", False)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

VALID_SUBJECTS = {"English", "Maths", "Science", "EVS", "Hindi", "Other"}
VALID_BOARDS = {"CBSE", "ICSE", "State Board", "Other"}


class ScoreRequest(BaseModel):
    text: str = Field(..., min_length=20, max_length=5000)
    subject: str = Field("English")

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, v):
        if v not in VALID_SUBJECTS:
            return "Other"
        return v


class FeedbackRequest(BaseModel):
    text: str = Field(..., min_length=20, max_length=5000)
    subject: str = Field("English")
    ari_grade_mid: int = Field(..., ge=1, le=10)
    teacher_grade: int = Field(..., ge=1, le=10)
    teacher_board: str = Field("CBSE")
    reason: str = Field("", max_length=1000)
    turnstile_token: str = Field(...)

    @field_validator("teacher_board")
    @classmethod
    def validate_board(cls, v):
        if v not in VALID_BOARDS:
            return "Other"
        return v


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"ok": True, "feedback_count": feedback_count()}


@app.post("/score")
@limiter.limit("10/minute")
def score(request: Request, body: ScoreRequest):
    """Score a passage. Returns grade range (e.g. Grade 3–5)."""
    words = body.text.split()
    if len(words) < 5:
        raise HTTPException(422, "Passage too short — please paste at least 5 words.")

    result = _predict_range(body.text, body.subject)
    return result


@app.post("/feedback")
@limiter.limit("5/minute")
async def feedback(request: Request, body: FeedbackRequest):
    """Store a teacher's grade rating for a passage."""
    ip = get_remote_address(request)

    # 1. Verify Turnstile CAPTCHA
    valid = await _verify_turnstile(body.turnstile_token, ip)
    if not valid:
        raise HTTPException(403, "CAPTCHA verification failed. Please try again.")

    # 2. DB size guard
    if not db_size_ok():
        raise HTTPException(503, "Feedback storage full. Contact acequest.in.")

    # 3. Dedup — same exact text already stored
    if is_duplicate(body.text):
        return {"ok": True, "note": "duplicate"}

    # 4. Re-score to get full range (in case frontend sent stale values)
    ari = _predict_range(body.text, body.subject)

    insert_feedback(
        text=body.text,
        subject=body.subject,
        ari_grade_low=ari["grade_low"],
        ari_grade_mid=ari["grade_mid"],
        ari_grade_high=ari["grade_high"],
        teacher_grade=body.teacher_grade,
        teacher_board=body.teacher_board,
        reason=body.reason,
    )

    return {"ok": True}
