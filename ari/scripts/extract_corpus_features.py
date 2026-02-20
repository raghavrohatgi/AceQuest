#!/usr/bin/env python3
"""
Phase 2.2 — Extract Features for Full Corpus
Runs FeatureExtractor over every segment in corpus-labelled.jsonl
and outputs a feature matrix CSV ready for model training.

Input:  /ari/data/corpus-labelled.jsonl
Output: /ari/data/corpus-features.csv

Columns: grade, subject, source,
          mean_word_frequency_rank, mean_sentence_length,
          type_token_ratio, avg_syllables_per_word, pct_rare_words,
          word_count, sentence_count

Run: python3 ari/scripts/extract_corpus_features.py
"""

import csv
import json
import sys
from pathlib import Path

# Allow running from project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ari.features import FeatureExtractor

DATA_DIR = Path("/Users/raghavrohatgi/Documents/AceQuest/ari/data")
INPUT_FILE = DATA_DIR / "corpus-labelled.jsonl"
OUTPUT_FILE = DATA_DIR / "corpus-features.csv"

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
    "word_count",
    "sentence_count",
]


def main():
    if not INPUT_FILE.exists():
        print(f"Error: {INPUT_FILE} not found. Run corpus_builder.py first.")
        sys.exit(1)

    print("Loading FeatureExtractor (reads NCERT data files)...")
    fe = FeatureExtractor()

    print(f"Loading corpus from {INPUT_FILE}...")
    records = []
    with open(INPUT_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    print(f"Extracting features for {len(records):,} segments...\n")

    rows = []
    skipped = 0

    for i, rec in enumerate(records):
        if i % 1000 == 0:
            print(f"  {i:,}/{len(records):,}", end="\r")

        grade = rec["grade"]
        subject = rec.get("subject", "")
        features = fe.extract(rec["text"], grade, subject=subject)

        # Skip degenerate segments — use grade-aware minimum
        min_wc = 5 if grade == 1 else (10 if grade == 2 else 10)
        if features["word_count"] < min_wc:
            skipped += 1
            continue

        row = {
            "grade": grade,
            "subject": rec.get("subject", ""),
            "source": rec.get("source", ""),
            **features,
        }
        rows.append(row)

    print(f"\n  Done. {len(rows):,} rows | {skipped} skipped (word_count < 10)\n")

    # Write CSV
    fieldnames = ["grade", "subject", "source"] + FEATURE_COLS
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"=== FEATURE EXTRACTION COMPLETE ===")
    print(f"Output : {OUTPUT_FILE}")
    print(f"Rows   : {len(rows):,}")

    # Per-grade summary
    from collections import defaultdict
    grade_stats: dict[int, list] = defaultdict(list)
    for row in rows:
        grade_stats[row["grade"]].append(row)

    print(f"\nPer-grade summary (mean values):")
    print(f"{'Grade':>6} {'N':>5} {'FreqRank':>10} {'SentLen':>9} {'TTR':>7} {'Sylls':>7} {'Rare%':>7}")
    print("-" * 55)

    for grade in sorted(grade_stats):
        recs = grade_stats[grade]
        n = len(recs)
        avg = lambda col: sum(r[col] for r in recs) / n
        print(
            f"{grade:>6} {n:>5} "
            f"{avg('mean_word_frequency_rank'):>10.1f} "
            f"{avg('mean_sentence_length'):>9.2f} "
            f"{avg('type_token_ratio'):>7.3f} "
            f"{avg('avg_syllables_per_word'):>7.3f} "
            f"{avg('pct_rare_words'):>7.1f}"
        )

    print("\nExpected: all 5 features should show upward trend with grade.")


if __name__ == "__main__":
    main()
