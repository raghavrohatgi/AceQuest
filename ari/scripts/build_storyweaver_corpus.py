#!/usr/bin/env python3
"""
Phase 1.2 — StoryWeaver Corpus Builder
Reads StoryWeaver MD files from ari/augmentation/storyweaver/,
extracts text segments, and appends them to corpus-labelled.jsonl.

Run: python3 ari/scripts/build_storyweaver_corpus.py
"""

import json
import re
from pathlib import Path

STORYWEAVER_DIR = Path("/Users/raghavrohatgi/Documents/AceQuest/ari/augmentation/storyweaver")
OUTPUT_DIR = Path("/Users/raghavrohatgi/Documents/AceQuest/ari/data")
OUTPUT_FILE = OUTPUT_DIR / "corpus-labelled.jsonl"

# StoryWeaver reading level → CBSE grade mapping
LEVEL_TO_GRADE = {1: 1, 2: 2, 3: 3, 4: 5, 5: 6}
MIN_WORDS = 20

# Skip lines that are just frontmatter, headings, or JS artefacts
RE_HEADING = re.compile(r"^\s*#{1,6}\s+")
RE_JS_ARTEFACT = re.compile(r"^\s*(var |function |if\(story_editor|\$\()")


def parse_frontmatter(text: str):
    """Parse YAML frontmatter, return (meta dict, body text)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = {}
    for line in parts[1].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"')
    return meta, parts[2].strip()


def extract_segments(text: str, min_words: int = MIN_WORDS):
    """Split body text into prose paragraph segments of at least min_words."""
    segments = []
    for para in re.split(r"\n{2,}", text):
        para = para.strip()
        if not para:
            continue
        # Skip headings and JS artefacts
        if RE_HEADING.match(para) or RE_JS_ARTEFACT.match(para):
            continue
        # Clean up leftover JS patterns within paragraph
        para = re.sub(r"\$\(document\)[\s\S]*?\}\);", " ", para)
        para = re.sub(r"\bvar\s+\w+[\s\S]*?;", " ", para)
        para = re.sub(r"\bif\s*\(story_editor[\s\S]*?\}\s*\);?", " ", para)
        para = re.sub(r"\s+", " ", para).strip()
        if len(para.split()) >= min_words:
            segments.append(para)
    return segments


def load_existing_keys(output_file: Path) -> set:
    """Load source keys already in the corpus to avoid duplicates."""
    keys = set()
    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if obj.get("source"):
                        keys.add(obj["source"])
                except json.JSONDecodeError:
                    pass
    return keys


def main():
    print("=== StoryWeaver Corpus Builder ===")
    print(f"Input: {STORYWEAVER_DIR}")
    print(f"Output: {OUTPUT_FILE}")

    existing_sources = load_existing_keys(OUTPUT_FILE)
    print(f"Existing corpus segments: {len(existing_sources)} sources already present")

    new_segments = 0
    skipped_dup = 0
    skipped_short = 0
    stories_processed = 0

    with open(OUTPUT_FILE, "a", encoding="utf-8") as out:
        for level in sorted([d.name for d in STORYWEAVER_DIR.iterdir()
                              if d.is_dir() and d.name.startswith("level-")]):
            level_num = int(level.split("-")[1])
            grade = LEVEL_TO_GRADE.get(level_num, level_num)
            level_dir = STORYWEAVER_DIR / level
            md_files = sorted(level_dir.glob("story-*.md"))

            level_segs = 0
            for md_file in md_files:
                source_key = f"StoryWeaver/{level}/{md_file.name}"
                if source_key in existing_sources:
                    skipped_dup += 1
                    continue

                text = md_file.read_text(encoding="utf-8")
                meta, body = parse_frontmatter(text)

                segments = extract_segments(body)
                if not segments:
                    skipped_short += 1
                    continue

                # For Level 1 stories (very short, ~100-150 words total),
                # treat the whole story as one segment if no paragraph is long enough
                if not segments:
                    words = body.split()
                    if len(words) >= MIN_WORDS:
                        segments = [" ".join(words)]

                for seg in segments:
                    record = {
                        "text": seg,
                        "grade": grade,
                        "subject": "English",
                        "source": source_key,
                    }
                    out.write(json.dumps(record) + "\n")
                    new_segments += 1
                    level_segs += 1

                stories_processed += 1

            print(f"  {level} (Grade {grade}): {len(md_files)} stories → {level_segs} segments")

    print(f"\nDone: {stories_processed} stories, {new_segments} new segments added to corpus")
    print(f"Skipped: {skipped_dup} already in corpus, {skipped_short} too short")

    # Print new total
    total = 0
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        total = sum(1 for _ in f)
    print(f"Total corpus segments now: {total:,}")


if __name__ == "__main__":
    main()
