#!/usr/bin/env python3
"""
Phase 1.2 — Build NCERT Word Frequency List
Tokenises all corpus prose and produces a ranked frequency list.

Input:  /ari/data/corpus-labelled.jsonl
Output: /ari/data/ncert-word-frequency.json
        [{"word": "the", "frequency": 18420, "rank": 1}, ...]

Run: python3 ari/scripts/build_frequency_list.py
"""

import json
import re
import string
from collections import Counter
from pathlib import Path

import nltk

# Download required NLTK data if missing
for pkg in ["punkt", "punkt_tab", "stopwords"]:
    try:
        nltk.data.find(f"tokenizers/{pkg}" if "punkt" in pkg else f"corpora/{pkg}")
    except LookupError:
        print(f"Downloading NLTK {pkg}...")
        nltk.download(pkg, quiet=True)

from nltk.tokenize import word_tokenize

DATA_DIR = Path("/Users/raghavrohatgi/Documents/AceQuest/ari/data")
INPUT_FILE = DATA_DIR / "corpus-labelled.jsonl"
OUTPUT_FILE = DATA_DIR / "ncert-word-frequency.json"

# Words to exclude from the frequency list entirely
EXCLUDE = set(string.punctuation) | {"formula", "reprint", "ncert", "cbse"}
RE_ALPHA = re.compile(r"^[a-zA-Z][a-zA-Z\-']*[a-zA-Z]$|^[a-zA-Z]$")


def is_content_word(token: str) -> bool:
    """Return True if this token should be counted in the frequency list."""
    t = token.lower().strip()
    if not t:
        return False
    if t in EXCLUDE:
        return False
    if not RE_ALPHA.match(t):
        return False
    if len(t) < 2:
        return False
    return True


def main():
    if not INPUT_FILE.exists():
        print(f"Error: {INPUT_FILE} not found. Run corpus_builder.py first.")
        return

    print(f"Loading corpus from {INPUT_FILE}...")
    records = []
    with open(INPUT_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    print(f"Tokenising {len(records):,} segments...")
    counter = Counter()

    for i, rec in enumerate(records):
        if i % 500 == 0:
            print(f"  {i:,}/{len(records):,}", end="\r")
        tokens = word_tokenize(rec["text"].lower())
        for tok in tokens:
            if is_content_word(tok):
                counter[tok] += 1

    print(f"\nUnique words found: {len(counter):,}")

    # Build ranked list sorted by frequency descending
    ranked = [
        {"word": word, "frequency": freq, "rank": rank}
        for rank, (word, freq) in enumerate(counter.most_common(), start=1)
    ]

    OUTPUT_FILE.write_text(json.dumps(ranked, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n=== FREQUENCY LIST BUILT ===")
    print(f"Total unique words : {len(ranked):,}")
    print(f"Output             : {OUTPUT_FILE}")
    print(f"\nTop 20 words:")
    for item in ranked[:20]:
        print(f"  #{item['rank']:3d}  {item['word']:<20} {item['frequency']:,}")


if __name__ == "__main__":
    main()
