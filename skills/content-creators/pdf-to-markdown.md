# Skill: pdf-to-markdown

## Purpose
Convert a single NCERT PDF chapter into clean, structured Markdown using Mistral OCR. This is the first step in the content pipeline. The output MD file becomes the permanent source of truth for all downstream question generation — never re-run OCR once you have a good MD file.

## Used By
- Pipeline Coordinator (Stage 0)

## Inputs

| Input | Type | Description |
|---|---|---|
| `pdf_path` | string | Absolute path to the source PDF (e.g. `/Books/CBSE Books Science/Class 6/Chapter 4 - Exploring Magnets.pdf`) |
| `output_path` | string | Destination MD file (e.g. `/Books-MD/Science/Class-6/ch04-exploring-magnets.md`) |
| `subject` | string | `math` / `english` / `science` |
| `grade` | integer | Class number (1–10) |

## Procedure

### Step 1: Run Mistral OCR

```python
from mistralai import Mistral
import os, pathlib

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

def convert_pdf_to_md(pdf_path: str, output_path: str):
    with open(pdf_path, "rb") as f:
        result = client.ocr.process(
            model="mistral-ocr-latest",
            document={"type": "pdf", "data": f.read()}
        )
    # Join pages with double newline separator
    md_content = "\n\n".join(page.markdown for page in result.pages)
    pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Converted: {pdf_path} → {output_path}")
```

### Step 2: Post-Processing Cleanup (Manual, one-time per file)

After OCR, open the MD file and fix:
- [ ] Remove running headers/footers (page numbers, "NCERT", chapter titles that repeat on every page)
- [ ] Verify math formulas are in LaTeX format: `$formula$` for inline, `$$formula$$` for block
- [ ] Check that `[DIAGRAM: ...]` placeholders describe what's shown (not just "image")
- [ ] Fix any table alignment issues
- [ ] Verify Hindi/Devanagari text rendered correctly (if present)

### Step 3: Add Metadata Header

Prepend the following YAML frontmatter to every MD file:

```markdown
---
subject: science
grade: 6
chapter_number: 4
chapter_title: "Exploring Magnets"
source_pdf: "CBSE Books Science/Class 6/Chapter 4 - Exploring Magnets.pdf"
converted_date: "2026-02-17"
conversion_tool: "mistral-ocr-latest"
manually_reviewed: false
---
```

Set `manually_reviewed: true` after completing Step 2.

### Step 4: Batch Conversion (All chapters)

```python
from concurrent.futures import ThreadPoolExecutor
import os

BOOK_DIR = "/Books"
MD_DIR = "/Books-MD"

# Map PDF paths to MD output paths
conversion_jobs = [
    # Science
    ("CBSE Books Science/Class 6/Chapter 1 - The Wonderful World of Science.pdf",
     "Science/Class-6/ch01-wonderful-world-of-science.md"),
    # ... add all chapters
]

def job(args):
    pdf_rel, md_rel = args
    convert_pdf_to_md(
        os.path.join(BOOK_DIR, pdf_rel),
        os.path.join(MD_DIR, md_rel)
    )

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(job, conversion_jobs)
```

## Output

A clean `.md` file at the specified `output_path` with:
- Proper heading hierarchy (`#`, `##`, `###`)
- LaTeX math formulas
- Markdown tables
- `[DIAGRAM: description]` placeholders for images
- YAML frontmatter with metadata

## Quality Checks

After conversion, verify:
- [ ] Word count is reasonable for the chapter length (100–3,000 words typical)
- [ ] No garbled characters or encoding errors
- [ ] Headings match the chapter structure
- [ ] At least one `[DIAGRAM: ...]` placeholder for Science/Math chapters that have figures
- [ ] YAML frontmatter is present and correct

## Example

**Input:** `/Books/CBSE Books Science/Class 6/Chapter 4 - Exploring Magnets.pdf`

**Output:** `/Books-MD/Science/Class-6/ch04-exploring-magnets.md`

```markdown
---
subject: science
grade: 6
chapter_number: 4
chapter_title: "Exploring Magnets"
source_pdf: "CBSE Books Science/Class 6/Chapter 4 - Exploring Magnets.pdf"
converted_date: "2026-02-17"
conversion_tool: "mistral-ocr-latest"
manually_reviewed: true
---

# Chapter 4: Exploring Magnets

## What is a Magnet?

A magnet is an object that attracts iron and certain other metals...

## Poles of a Magnet

Every magnet has two poles — the **North Pole** and the **South Pole**.

[DIAGRAM: Bar magnet showing N and S poles with magnetic field lines drawn around it]

## Magnetic and Non-Magnetic Materials

| Magnetic | Non-Magnetic |
|---|---|
| Iron | Wood |
| Nickel | Plastic |
| Cobalt | Glass |

## Key Rules

- Like poles **repel** each other
- Unlike poles **attract** each other
```

## Notes
- Run OCR only once per PDF. Store the MD file permanently.
- If a chapter's MD quality is poor after OCR, try splitting the PDF into individual pages before re-running.
- Cost: ~$0.001/page via Mistral API → entire `/Books/` library costs ~$3 total.
