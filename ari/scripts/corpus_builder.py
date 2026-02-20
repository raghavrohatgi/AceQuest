#!/usr/bin/env python3
"""
Phase 1.1 — Corpus Builder
Walks Books-MD/, strips non-prose content, extracts labelled text segments.

Output: /ari/data/corpus-labelled.jsonl
Each line: {"text": "...", "grade": 6, "subject": "Science", "source": "Class-6/Chapter-01-...md"}

Run: python3 ari/scripts/corpus_builder.py
"""

import json
import re
import sys
from pathlib import Path

BOOKS_MD = Path("/Users/raghavrohatgi/Documents/AceQuest/Books-MD")
OUTPUT_DIR = Path("/Users/raghavrohatgi/Documents/AceQuest/ari/data")
OUTPUT_FILE = OUTPUT_DIR / "corpus-labelled.jsonl"

MIN_WORDS = 20        # minimum words for a paragraph to be included (grades 3+)
MIN_WORDS_G2 = 10     # lower threshold for grade 2
MIN_WORDS_G1 = 5      # lowest threshold for grade 1 (very short early reader sentences)
MIN_CHARS = 80        # minimum characters (fast pre-filter before word count)

# === Patterns to strip ===

# Lines that are purely image references
RE_IMAGE = re.compile(r"^\s*!\[.*?\]\(.*?\)\s*$")

# Lines that are headings (#, ##, etc.)
RE_HEADING = re.compile(r"^\s*#{1,6}\s+")

# YAML frontmatter (handled separately by splitting on ---)
# Reprint lines (page markers)
RE_REPRINT = re.compile(r"^Reprint\s+\d{4}-\d{2,4}\s*$", re.IGNORECASE)

# NCERT chapter code stamps (e.g. "0124CH03", "0677CH01")
RE_NCERT_CODE = re.compile(r"^\s*[0-9]{4}CH[0-9]+\s*$")

# Pure page numbers (single digit or small number on its own line)
RE_PAGE_NUMBER = re.compile(r"^\s*\d{1,3}\s*$")

# Exercise/question patterns — lines that start these blocks
RE_EXERCISE_START = re.compile(
    r"^\s*(\*{0,2})(Exercise|Activity|Think and Discuss|Let['']s Discuss|"
    r"Q\.|Q\s*\d|Question\s*\d|\d+\.\s+[A-Z]|Fill in the [Bb]lanks|"
    r"True or False|Match the [Ff]ollowing|Answer the [Ff]ollowing|"
    r"Thinking about the Text|Thinking about Language|"
    r"Before You Read|Working with the Text|Working with Language|"
    r"Speaking and Writing|Do and Learn|Do it [Yy]ourself|"
    r"Try [Tt]his|Intext Question|In-text Question)",
    re.IGNORECASE,
)

# Bullet/list lines that are short exercise items (not prose)
RE_BULLET = re.compile(r"^\s*[-*•]\s+")

# LaTeX math blocks
RE_LATEX_INLINE = re.compile(r"\$[^$]+\$")
RE_LATEX_BLOCK = re.compile(r"\$\$[\s\S]+?\$\$")

# Image caption-only lines (just short text after an image, ≤6 words)
# These get filtered by MIN_WORDS anyway

# Score/fraction/formula fragments
RE_FORMULA_ONLY = re.compile(r"^[\s\d\+\-\*/=<>%.,()°{}|\\]+$")

# "X / BookName" page markers (e.g. "2 / Beehive", "Notes for the Teacher / 3")
RE_BOOK_PAGE_MARKER = re.compile(r"^\s*[\w\s]+/\s*\d+\s*$|^\s*\d+\s*/\s*[\w\s]+\s*$")


def strip_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from body. Returns (meta_dict, body_text)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta_block = parts[1]
    body = parts[2].strip()
    meta = {}
    for line in meta_block.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip('"')
    return meta, body


def is_prose_paragraph(para: str, min_words: int = MIN_WORDS) -> bool:
    """Return True if this paragraph looks like readable prose."""
    lines = para.strip().splitlines()
    if not lines:
        return False

    # Check each line — if most lines are skip-worthy, reject the whole paragraph
    prose_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if RE_IMAGE.match(line):
            continue
        if RE_HEADING.match(line):
            return False  # whole para is a heading
        if RE_REPRINT.match(line):
            continue
        if RE_NCERT_CODE.match(line):
            continue
        if RE_PAGE_NUMBER.match(line):
            continue
        if RE_BOOK_PAGE_MARKER.match(line):
            continue
        if RE_FORMULA_ONLY.match(line):
            continue
        if RE_EXERCISE_START.match(line):
            return False
        prose_lines.append(line)

    if not prose_lines:
        return False

    text = " ".join(prose_lines)

    # Remove inline LaTeX before word counting
    text = RE_LATEX_INLINE.sub(" ", text)
    text = RE_LATEX_BLOCK.sub(" ", text)

    # Word count gate
    words = text.split()
    if len(words) < min_words:
        return False

    # Reject if >40% of words are numbers/symbols (math-heavy)
    alpha_words = [w for w in words if any(c.isalpha() for c in w)]
    if len(alpha_words) < len(words) * 0.6:
        return False

    return True


def clean_paragraph(para: str) -> str:
    """Clean a prose paragraph for corpus use."""
    lines = []
    for line in para.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if RE_IMAGE.match(line):
            continue
        if RE_REPRINT.match(line):
            continue
        if RE_NCERT_CODE.match(line):
            continue
        if RE_PAGE_NUMBER.match(line):
            continue
        if RE_BOOK_PAGE_MARKER.match(line):
            continue
        if RE_FORMULA_ONLY.match(line):
            continue
        lines.append(line)

    text = " ".join(lines)
    # Remove inline LaTeX
    text = RE_LATEX_INLINE.sub(" [formula] ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_prose_from_md(md_path: Path, min_words: int = MIN_WORDS) -> list[str]:
    """Extract clean prose paragraphs from a single MD file."""
    raw = md_path.read_text(encoding="utf-8", errors="replace")
    meta, body = strip_frontmatter(raw)

    # Split into paragraphs on blank lines
    raw_paragraphs = re.split(r"\n\s*\n", body)

    prose = []
    in_exercise_block = False

    for para in raw_paragraphs:
        para = para.strip()
        if not para:
            continue

        # Detect exercise block start — once we see it, skip until next heading
        first_line = para.splitlines()[0].strip()
        if RE_EXERCISE_START.match(first_line):
            in_exercise_block = True
            continue

        # A new top-level heading resets exercise block suppression
        if RE_HEADING.match(first_line) and first_line.startswith("# "):
            in_exercise_block = False
            continue
        if RE_HEADING.match(first_line):
            # Sub-headings: only reset if it looks like a new story/chapter section
            in_exercise_block = False
            continue

        if in_exercise_block:
            continue

        if not is_prose_paragraph(para, min_words=min_words):
            continue

        cleaned = clean_paragraph(para)
        if len(cleaned.split()) >= min_words:
            prose.append(cleaned)

    return prose


def process_all_files() -> list[dict]:
    """Walk Books-MD, extract prose segments, return labelled records."""
    md_files = [
        f for f in sorted(BOOKS_MD.rglob("*.md"))
        if f.name != "_conversion_log.json" and not f.name.startswith("_")
    ]

    records = []
    stats = {"files": 0, "segments": 0, "by_grade": {}}

    print(f"Processing {len(md_files)} MD files...\n")

    for md_path in md_files:
        # Read frontmatter for grade/subject
        raw = md_path.read_text(encoding="utf-8", errors="replace")
        meta, _ = strip_frontmatter(raw)

        grade_str = meta.get("grade", "")
        subject = meta.get("subject", "Unknown")

        try:
            grade = int(grade_str)
        except (ValueError, TypeError):
            print(f"  ⚠ No grade found: {md_path.name}, skipping")
            continue

        if grade == 1:
            min_words = MIN_WORDS_G1
        elif grade == 2:
            min_words = MIN_WORDS_G2
        else:
            min_words = MIN_WORDS
        paragraphs = extract_prose_from_md(md_path, min_words=min_words)

        if not paragraphs:
            print(f"  ⚠ No prose extracted: {md_path.relative_to(BOOKS_MD)}")
            continue

        source = str(md_path.relative_to(BOOKS_MD))
        for para in paragraphs:
            records.append({
                "text": para,
                "grade": grade,
                "subject": subject,
                "source": source,
            })

        stats["files"] += 1
        stats["segments"] += len(paragraphs)
        stats["by_grade"][grade] = stats["by_grade"].get(grade, 0) + len(paragraphs)

    return records, stats


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    records, stats = process_all_files()

    # Write JSONL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"\n=== CORPUS BUILD COMPLETE ===")
    print(f"Files processed : {stats['files']}")
    print(f"Total segments  : {stats['segments']}")
    print(f"Output          : {OUTPUT_FILE}")
    print(f"\nSegments per grade:")
    for grade in sorted(stats["by_grade"]):
        count = stats["by_grade"][grade]
        bar = "█" * min(count // 10, 60)
        flag = " ⚠ LOW" if count < 200 else ""
        print(f"  Grade {grade:2d}: {count:4d}  {bar}{flag}")

    # Warn on grades with very few segments
    low_grades = [g for g, c in stats["by_grade"].items() if c < 200]
    if low_grades:
        print(f"\n⚠ Low segment count for grades: {sorted(low_grades)}")
        print("  Consider including more chapters or lowering MIN_WORDS threshold.")


if __name__ == "__main__":
    main()
