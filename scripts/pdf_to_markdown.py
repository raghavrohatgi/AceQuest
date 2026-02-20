#!/usr/bin/env python3
"""
PDF to Markdown converter using Mistral OCR API.
Converts CBSE textbook PDFs from /Books/ to /Books-MD/ with YAML frontmatter.

Usage:
  python3 pdf_to_markdown.py --pilot      # Run on 5 representative chapters
  python3 pdf_to_markdown.py --full       # Run on all chapters
  python3 pdf_to_markdown.py --file PATH  # Run on a single file
"""

import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "U3yFl9l4eHaXoAsMXDYVRlZ7mGC79Ccz")
BOOKS_DIR = Path("/Users/raghavrohatgi/Documents/AceQuest/Books")
OUTPUT_DIR = Path("/Users/raghavrohatgi/Documents/AceQuest/Books-MD")

# Subject name normalisation
SUBJECT_MAP = {
    "CBSE Books English": "English",
    "CBSE Books Maths": "Maths",
    "CBSE Books Science": "Science",
}

# Files to skip (cover pages, prescription sheets, non-chapter files)
SKIP_PATTERNS = [
    r"ps\.pdf$",           # prescription sheets
    r"cc\.pdf$",           # cover pages
    r"^\w{6,8}\.pdf$",    # short alphanumeric filenames (NCERT codes)
]

# Pilot: 5 representative chapters (1 per subject/grade combo)
PILOT_FILES = [
    "CBSE Books English/Class 1/Chapter 01 - Two Little Hands.pdf",
    "CBSE Books English/Class 9/Beehive/Chapter 01 - The Fun They Had.pdf",
    "CBSE Books Maths/Class 6/Chapter 01 - Knowing Our Numbers.pdf",
    "CBSE Books Science/Class 6/Chapter 1 - The Wonderful World of Science.pdf",
    "CBSE Books Science/Class 10/Chapter 1 - Chemical Reactions And Equations.pdf",
]


def should_skip(filename: str) -> bool:
    """Return True if this file should be skipped (not a chapter)."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, filename, re.IGNORECASE):
            return True
    return False


def parse_path(pdf_path: Path) -> dict:
    """Extract subject, grade, book, chapter_number, chapter_title from path."""
    parts = pdf_path.relative_to(BOOKS_DIR).parts
    subject_raw = parts[0]
    subject = SUBJECT_MAP.get(subject_raw, subject_raw)

    # Extract class number
    class_part = parts[1] if len(parts) > 1 else "Unknown"
    grade_match = re.search(r"Class\s+(\d+)", class_part, re.IGNORECASE)
    grade = int(grade_match.group(1)) if grade_match else 0

    # Book name (subdirectory if present, e.g. "Beehive", "Moments")
    book = ""
    filename = pdf_path.stem
    if len(parts) == 4:  # Subject/Class/Book/Chapter.pdf
        book = parts[2]
    elif len(parts) == 3 and "Part" in parts[2]:
        book = parts[2]

    # Chapter number and title from filename
    chapter_match = re.match(r"Chapter\s+0*(\d+)\s*[-–]\s*(.+)", filename, re.IGNORECASE)
    if chapter_match:
        chapter_number = int(chapter_match.group(1))
        chapter_title = chapter_match.group(2).strip()
    else:
        chapter_number = 0
        chapter_title = filename

    return {
        "subject": subject,
        "grade": grade,
        "book": book,
        "chapter_number": chapter_number,
        "chapter_title": chapter_title,
    }


def build_output_path(pdf_path: Path, meta: dict) -> Path:
    """Build the output .md path under Books-MD/."""
    subject = meta["subject"]
    grade = meta["grade"]
    book = meta["book"]
    chapter_num = meta["chapter_number"]
    chapter_title = meta["chapter_title"]

    # Sanitise chapter title for filename
    safe_title = re.sub(r'[^\w\s-]', '', chapter_title).strip()
    safe_title = re.sub(r'\s+', '-', safe_title)

    if chapter_num > 0:
        filename = f"Chapter-{chapter_num:02d}-{safe_title}.md"
    else:
        filename = f"{safe_title}.md"

    if book:
        return OUTPUT_DIR / subject / f"Class-{grade}" / book / filename
    else:
        return OUTPUT_DIR / subject / f"Class-{grade}" / filename


def build_frontmatter(meta: dict, pdf_path: Path) -> str:
    """Build YAML frontmatter for the markdown file."""
    lines = [
        "---",
        f'subject: "{meta["subject"]}"',
        f'grade: {meta["grade"]}',
    ]
    if meta["book"]:
        lines.append(f'book: "{meta["book"]}"')
    lines += [
        f'chapter_number: {meta["chapter_number"]}',
        f'chapter_title: "{meta["chapter_title"]}"',
        f'source_pdf: "{pdf_path.relative_to(BOOKS_DIR)}"',
        f'ocr_tool: "mistral-ocr-latest"',
        "---\n",
    ]
    return "\n".join(lines)


def ocr_pdf_with_mistral(pdf_path: Path, max_retries: int = 5) -> str:
    """Send PDF to Mistral OCR API and return markdown text. Retries on transient errors."""
    from mistralai import Mistral

    client = Mistral(api_key=MISTRAL_API_KEY)

    for attempt in range(1, max_retries + 1):
        uploaded_id = None
        try:
            # Upload the file to Mistral files API
            with open(pdf_path, "rb") as f:
                uploaded = client.files.upload(
                    file={"file_name": pdf_path.name, "content": f, "mime_type": "application/pdf"},
                    purpose="ocr",
                )
            uploaded_id = uploaded.id

            # Get a signed URL for the uploaded file
            signed = client.files.get_signed_url(file_id=uploaded_id, expiry=60)

            # Run OCR
            response = client.ocr.process(
                model="mistral-ocr-latest",
                document={"type": "document_url", "document_url": signed.url},
                include_image_base64=False,
            )

            # Concatenate pages
            pages = response.pages if hasattr(response, "pages") else []
            markdown_parts = []
            for page in pages:
                if hasattr(page, "markdown") and page.markdown:
                    markdown_parts.append(page.markdown.strip())

            return "\n\n".join(markdown_parts)

        except Exception as e:
            err_str = str(e)
            # Clean up uploaded file if we have the ID
            if uploaded_id:
                try:
                    client.files.delete(file_id=uploaded_id)
                except Exception:
                    pass

            is_transient = any(code in err_str for code in ["500", "502", "503", "520", "429"])
            if is_transient and attempt < max_retries:
                wait = 2 ** attempt  # 2, 4, 8, 16, 32 seconds
                print(f"    ⟳ Transient error (attempt {attempt}/{max_retries}), retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise  # Non-transient or exhausted retries


def convert_pdf(pdf_path: Path, dry_run: bool = False) -> dict:
    """Convert a single PDF to Markdown. Returns status dict."""
    if should_skip(pdf_path.name):
        return {"status": "skipped", "path": str(pdf_path)}

    meta = parse_path(pdf_path)
    out_path = build_output_path(pdf_path, meta)

    if out_path.exists():
        return {"status": "already_exists", "path": str(out_path)}

    if dry_run:
        return {"status": "dry_run", "would_write": str(out_path), "meta": meta}

    print(f"  OCR: {pdf_path.relative_to(BOOKS_DIR)}")
    try:
        markdown_content = ocr_pdf_with_mistral(pdf_path)
        frontmatter = build_frontmatter(meta, pdf_path)
        full_content = frontmatter + "\n" + markdown_content

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(full_content, encoding="utf-8")

        word_count = len(markdown_content.split())
        print(f"  ✓ Written: {out_path.relative_to(OUTPUT_DIR)} ({word_count:,} words)")
        return {"status": "success", "path": str(out_path), "word_count": word_count}

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return {"status": "error", "path": str(pdf_path), "error": str(e)}


def get_all_chapter_pdfs() -> list[Path]:
    """Return all chapter PDF paths, excluding skip patterns."""
    all_pdfs = sorted(BOOKS_DIR.rglob("*.pdf"))
    return [p for p in all_pdfs if not should_skip(p.name)]


def run_pilot():
    """Run OCR on 5 representative pilot chapters."""
    print("\n=== PILOT RUN (5 chapters) ===\n")
    results = []
    for rel_path in PILOT_FILES:
        pdf_path = BOOKS_DIR / rel_path
        if not pdf_path.exists():
            # Try to find a close match
            subject_dir = BOOKS_DIR / Path(rel_path).parts[0]
            print(f"  ⚠ Not found: {rel_path}")
            print(f"    Looking in {subject_dir}...")
            # Find first chapter in the same class dir
            class_dir = pdf_path.parent
            candidates = sorted(class_dir.glob("Chapter*.pdf")) if class_dir.exists() else []
            if candidates:
                pdf_path = candidates[0]
                print(f"    Using: {pdf_path.name}")
            else:
                results.append({"status": "not_found", "path": rel_path})
                continue

        result = convert_pdf(pdf_path)
        results.append(result)
        time.sleep(0.5)  # gentle rate limiting

    print("\n=== PILOT RESULTS ===")
    for r in results:
        status = r.get("status", "?")
        path = r.get("path", r.get("would_write", "?"))
        words = r.get("word_count", "")
        suffix = f" | {words:,} words" if isinstance(words, int) else ""
        print(f"  [{status}] {path}{suffix}")

    success_count = sum(1 for r in results if r["status"] == "success")
    print(f"\n{success_count}/{len(results)} pilot files converted successfully.")
    return results


def run_full_batch():
    """Run OCR on all chapter PDFs."""
    all_pdfs = get_all_chapter_pdfs()
    print(f"\n=== FULL BATCH ({len(all_pdfs)} chapters) ===\n")

    results = []
    success = skipped = errors = already = 0

    for i, pdf_path in enumerate(all_pdfs, 1):
        print(f"[{i}/{len(all_pdfs)}]", end=" ")
        result = convert_pdf(pdf_path)
        results.append(result)

        s = result["status"]
        if s == "success":
            success += 1
        elif s in ("skipped",):
            skipped += 1
        elif s == "already_exists":
            already += 1
        else:
            errors += 1

        # Save progress log after each file
        log_path = OUTPUT_DIR / "_conversion_log.json"
        log_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

        if s == "success":
            time.sleep(0.3)  # rate limiting between API calls

    print(f"\n=== BATCH COMPLETE ===")
    print(f"  Success:       {success}")
    print(f"  Already done:  {already}")
    print(f"  Skipped:       {skipped}")
    print(f"  Errors:        {errors}")
    print(f"  Log saved:     {log_path}")
    return results


def run_single(file_path: str):
    """Convert a single PDF file."""
    pdf_path = Path(file_path)
    if not pdf_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    print(f"\n=== SINGLE FILE: {pdf_path.name} ===\n")
    result = convert_pdf(pdf_path)
    print(f"\nResult: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CBSE PDFs to Markdown via Mistral OCR")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pilot", action="store_true", help="Run on 5 pilot chapters")
    group.add_argument("--full", action="store_true", help="Run on all chapters")
    group.add_argument("--file", type=str, help="Run on a single PDF file")
    group.add_argument("--list", action="store_true", help="List all chapter PDFs (dry run)")
    args = parser.parse_args()

    if args.pilot:
        run_pilot()
    elif args.full:
        run_full_batch()
    elif args.file:
        run_single(args.file)
    elif args.list:
        pdfs = get_all_chapter_pdfs()
        for p in pdfs:
            print(p.relative_to(BOOKS_DIR))
        print(f"\nTotal: {len(pdfs)} chapter PDFs")
