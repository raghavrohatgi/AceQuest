#!/usr/bin/env python3
"""
Phase 1.3 — Build Grade Vocabulary Lists
Produces two outputs:

1. grade-vocab-lists.json     — per-grade top-500 (grades 1–10 individually)
2. grade-band-vocab-lists.json — per-band top-500 (1-3, 4-6, 7-10) for fast lookup

The per-grade lists use a "cumulative" strategy: grade N includes all words
from grades 1..N that have appeared in the corpus. This means a word familiar
at Grade 3 is also considered familiar at Grade 6. The `pct_rare_words` feature
then measures words NOT in the cumulative vocab for that grade.

Input:  /ari/data/corpus-labelled.jsonl
Output: /ari/data/grade-vocab-lists.json
        /ari/data/grade-band-vocab-lists.json

Run: python3 ari/scripts/build_vocab_lists.py
"""

import json
import re
import string
from collections import Counter
from pathlib import Path

import nltk

for pkg in ["punkt", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)

from nltk.tokenize import word_tokenize

DATA_DIR = Path("/Users/raghavrohatgi/Documents/AceQuest/ari/data")
INPUT_FILE = DATA_DIR / "corpus-labelled.jsonl"
OUTPUT_PER_GRADE = DATA_DIR / "grade-vocab-lists.json"
OUTPUT_PER_GRADE_SUBJECT = DATA_DIR / "grade-subject-vocab-lists.json"
OUTPUT_PER_BAND = DATA_DIR / "grade-band-vocab-lists.json"

ALL_GRADES = list(range(1, 11))  # 1 through 10
ALL_SUBJECTS = ["English", "Maths", "Science"]

GRADE_BANDS = {
    "1-3": [1, 2, 3],
    "4-6": [4, 5, 6],
    "7-10": [7, 8, 9, 10],
}

TOP_N = 1000  # bumped from 500 — larger vocab = more discriminative rare-word signal

EXCLUDE = set(string.punctuation) | {"formula", "reprint", "ncert", "cbse"}
RE_ALPHA = re.compile(r"^[a-zA-Z][a-zA-Z\-']*[a-zA-Z]$|^[a-zA-Z]$")


def is_content_word(token: str) -> bool:
    t = token.lower().strip()
    if not t or t in EXCLUDE or not RE_ALPHA.match(t) or len(t) < 2:
        return False
    return True


def main():
    if not INPUT_FILE.exists():
        print(f"Error: {INPUT_FILE} not found. Run corpus_builder.py first.")
        return

    print(f"Loading corpus...")
    records = []
    with open(INPUT_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    # Build per-grade AND per-grade-subject word counters
    grade_counters = {g: Counter() for g in ALL_GRADES}
    grade_subject_counters = {
        f"{g}_{s}": Counter() for g in ALL_GRADES for s in ALL_SUBJECTS
    }

    print(f"Tokenising {len(records):,} segments by grade and subject...")
    for rec in records:
        grade = rec["grade"]
        subject = rec.get("subject", "")
        if grade not in grade_counters:
            continue
        tokens = word_tokenize(rec["text"].lower())
        content_toks = [t for t in tokens if is_content_word(t)]
        for tok in content_toks:
            grade_counters[grade][tok] += 1
            key = f"{grade}_{subject}"
            if key in grade_subject_counters:
                grade_subject_counters[key][tok] += 1

    # Per-grade cumulative vocab: grade N = top-500 from grades 1..N combined
    # This reflects what a student at grade N has already been exposed to
    print(f"\n=== PER-GRADE VOCABULARY (cumulative) ===")
    per_grade = {}
    cumulative_counter: Counter = Counter()

    for grade in ALL_GRADES:
        cumulative_counter += grade_counters[grade]
        top_words = [word for word, _ in cumulative_counter.most_common(TOP_N)]
        per_grade[str(grade)] = top_words
        unique_at_grade = len(grade_counters[grade])
        print(f"  Grade {grade:2d}: {unique_at_grade:,} unique words in grade | cumulative top-{TOP_N}: {top_words[TOP_N-5:TOP_N]}")

    OUTPUT_PER_GRADE.write_text(json.dumps(per_grade, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nPer-grade output: {OUTPUT_PER_GRADE}")

    # Per-band vocab (non-cumulative, independent bands) — kept for backward compat
    print(f"\n=== PER-BAND VOCABULARY (independent) ===")
    per_band = {}
    for band, grades in GRADE_BANDS.items():
        band_counter: Counter = Counter()
        for g in grades:
            band_counter += grade_counters[g]
        top_words = [word for word, _ in band_counter.most_common(TOP_N)]
        per_band[band] = top_words
        print(f"  Band {band}: {len(band_counter):,} unique words → top {len(top_words)} saved")
        print(f"    Sample #490-500: {top_words[489:499]}")

    OUTPUT_PER_BAND.write_text(json.dumps(per_band, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nPer-band output: {OUTPUT_PER_BAND}")

    # Per-grade-subject vocab (cumulative within subject per grade)
    print(f"\n=== PER-GRADE-SUBJECT VOCABULARY (cumulative within subject) ===")
    per_grade_subject = {}
    for subject in ALL_SUBJECTS:
        cumulative: Counter = Counter()
        for grade in ALL_GRADES:
            key = f"{grade}_{subject}"
            cumulative += grade_subject_counters[key]
            top_words = [word for word, _ in cumulative.most_common(TOP_N)]
            per_grade_subject[f"{grade}_{subject}"] = top_words
        print(f"  {subject}: grades 1-10 built (top-{TOP_N} cumulative per grade)")

    OUTPUT_PER_GRADE_SUBJECT.write_text(
        json.dumps(per_grade_subject, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nPer-grade-subject output: {OUTPUT_PER_GRADE_SUBJECT}")


if __name__ == "__main__":
    main()
