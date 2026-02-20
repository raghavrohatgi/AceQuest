# Skill: validate-markdown

## Purpose
After Mistral OCR converts a PDF chapter to Markdown, validate that the output is usable for downstream tasks (corpus labelling, feature extraction, question generation). Catches garbled text, broken structure, missing frontmatter, and formula corruption before bad data enters the pipeline.

## Used By
- PDF-to-MD Agent (Stage 0, after conversion)
- ARI Corpus Preparation (prerequisite gate)

## Inputs

| Input | Type | Description |
|---|---|---|
| `md_file_path` | string | Path to the converted MD file |
| `expected_grade` | integer | Class number (1–10) |
| `expected_subject` | string | `math` / `english` / `science` |
| `expected_chapter` | integer | Chapter number |

## Procedure

### Step 1 — Automated Structural Checks

Run these programmatically before any human review:

```python
import re
import yaml
import json
from pathlib import Path

def validate_markdown(md_file_path: str, expected_grade: int, expected_subject: str, expected_chapter: int) -> dict:
    path = Path(md_file_path)
    content = path.read_text(encoding="utf-8")
    issues = []
    warnings = []

    # --- 1. YAML Frontmatter ---
    frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        issues.append("MISSING_FRONTMATTER: No YAML frontmatter found")
        frontmatter = {}
    else:
        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
        except yaml.YAMLError as e:
            issues.append(f"BROKEN_FRONTMATTER: YAML parse error — {e}")
            frontmatter = {}

    # --- 2. Frontmatter field completeness ---
    required_fields = ["grade", "subject", "chapter_number", "chapter_title", "source"]
    for field in required_fields:
        if field not in frontmatter:
            issues.append(f"MISSING_FIELD: frontmatter.{field} is absent")

    # --- 3. Grade / subject / chapter match ---
    if frontmatter.get("grade") != expected_grade:
        issues.append(f"GRADE_MISMATCH: frontmatter says {frontmatter.get('grade')}, expected {expected_grade}")
    if frontmatter.get("subject", "").lower() != expected_subject.lower():
        issues.append(f"SUBJECT_MISMATCH: frontmatter says {frontmatter.get('subject')}, expected {expected_subject}")
    if frontmatter.get("chapter_number") != expected_chapter:
        issues.append(f"CHAPTER_MISMATCH: frontmatter says {frontmatter.get('chapter_number')}, expected {expected_chapter}")

    # --- 4. Word count plausibility ---
    body = content[frontmatter_match.end():] if frontmatter_match else content
    words = body.split()
    word_count = len(words)

    # Expected range by grade band (prose only, approximate)
    expected_ranges = {
        range(1, 4): (300, 1500),    # Classes 1–3: short chapters
        range(4, 7): (800, 3000),    # Classes 4–6: medium chapters
        range(7, 11): (1500, 5000),  # Classes 7–10: longer, denser chapters
    }
    expected_min, expected_max = 300, 5000
    for grade_range, (lo, hi) in expected_ranges.items():
        if expected_grade in grade_range:
            expected_min, expected_max = lo, hi

    if word_count < expected_min:
        issues.append(f"TOO_SHORT: {word_count} words (expected ≥ {expected_min} for Class {expected_grade})")
    elif word_count > expected_max:
        warnings.append(f"UNUSUALLY_LONG: {word_count} words (expected ≤ {expected_max}). Check for duplicate content or merged chapters.")

    # --- 5. Heading structure ---
    headings = re.findall(r"^#{1,4} .+", body, re.MULTILINE)
    if len(headings) < 2:
        warnings.append(f"FEW_HEADINGS: Only {len(headings)} headings found. Chapter may not be properly structured.")

    # --- 6. Garbled text detection ---
    # Heuristic: high ratio of non-ASCII characters in non-formula blocks
    non_formula_body = re.sub(r"\$.*?\$", "", body, flags=re.DOTALL)  # strip inline formulas
    non_formula_body = re.sub(r"\$\$.*?\$\$", "", non_formula_body, flags=re.DOTALL)  # strip block formulas
    non_ascii_count = sum(1 for c in non_formula_body if ord(c) > 127)
    non_ascii_ratio = non_ascii_count / max(1, len(non_formula_body))
    if non_ascii_ratio > 0.05:
        issues.append(f"HIGH_NON_ASCII: {non_ascii_ratio:.1%} non-ASCII characters outside formulas — likely garbled OCR")

    # --- 7. Repeated character blocks (OCR artefact) ---
    repeated = re.findall(r"(.)\1{6,}", body)
    if repeated:
        issues.append(f"REPEATED_CHARS: Found repeated character sequences ({len(repeated)} instances) — OCR artefact")

    # --- 8. Formula preservation (Math chapters) ---
    formula_count = len(re.findall(r"\$", body)) // 2
    if expected_subject == "math" and formula_count < 5:
        warnings.append(f"FEW_FORMULAS: Only {formula_count} LaTeX formulas detected in a Math chapter — formulas may have been dropped")

    # --- 9. Exercise section separation ---
    has_exercise_marker = bool(re.search(r"##\s*(exercise|exercises|activity|think and discuss|solved example)", body, re.IGNORECASE))
    if not has_exercise_marker:
        warnings.append("NO_EXERCISE_MARKER: Could not find an exercise/activity section heading. Verify prose is not mixed with exercises.")

    # --- 10. Determine result ---
    status = "PASS" if not issues else "FAIL"

    return {
        "file": md_file_path,
        "status": status,
        "word_count": word_count,
        "formula_count": formula_count,
        "heading_count": len(headings),
        "issues": issues,          # blockers — file must not enter pipeline until resolved
        "warnings": warnings,      # advisory — human should check but not auto-blocked
        "frontmatter_parsed": frontmatter
    }
```

---

### Step 2 — Semantic Spot-Check (AI-assisted)

For every 10th file (or any file that passed Step 1 with warnings), run an AI semantic check:

**Prompt to Claude:**

```
You are validating a Markdown conversion of an NCERT Class [GRADE] [SUBJECT] chapter.

Below is the first 500 words of the converted chapter. Check for:
1. Is this recognisably a Class [GRADE] [SUBJECT] NCERT chapter? (Yes / Uncertain / No)
2. Does the prose read naturally, or does it appear garbled / broken? (Natural / Partially garbled / Garbled)
3. Are there any obvious OCR errors — wrong words, merged words, missing spaces? List up to 5 examples.
4. Does the difficulty level feel appropriate for Class [GRADE]? (Yes / Too Easy / Too Hard)

Chapter excerpt:
[FIRST_500_WORDS]

Respond in JSON:
{
  "looks_like_ncert": true/false,
  "prose_quality": "natural" | "partial_garble" | "garbled",
  "ocr_errors_found": ["example1", "example2"],
  "difficulty_appropriate": true/false,
  "notes": "..."
}
```

**Decision rule:**
- If `prose_quality = "garbled"` → fail, re-run OCR with different settings
- If `prose_quality = "partial_garble"` → flag for human review before corpus use
- If `prose_quality = "natural"` → pass semantic check

---

### Step 3 — Cross-Reference Check

Verify chapter completeness against the source chapter list:

```python
def cross_reference_check(md_file_path: str, chapter_manifest: dict) -> dict:
    """
    chapter_manifest: { "grade": 6, "subject": "science", "chapter": 4,
                         "expected_title": "Magnets", "expected_word_range": [1800, 2500] }
    """
    import yaml, re
    from pathlib import Path

    content = Path(md_file_path).read_text()
    fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    frontmatter = yaml.safe_load(fm_match.group(1)) if fm_match else {}

    body = content[fm_match.end():] if fm_match else content
    word_count = len(body.split())

    title_match = chapter_manifest["expected_title"].lower() in frontmatter.get("chapter_title", "").lower()
    in_word_range = chapter_manifest["expected_word_range"][0] <= word_count <= chapter_manifest["expected_word_range"][1]

    return {
        "title_matches": title_match,
        "word_count_in_range": in_word_range,
        "word_count": word_count,
        "frontmatter_title": frontmatter.get("chapter_title"),
    }
```

---

### Step 4 — Batch Validation Report

After validating all chapters, produce a summary:

```python
def batch_validation_report(results: list) -> dict:
    passed = [r for r in results if r["status"] == "PASS"]
    failed = [r for r in results if r["status"] == "FAIL"]
    warned = [r for r in results if r["status"] == "PASS" and r["warnings"]]

    return {
        "total": len(results),
        "passed": len(passed),
        "failed": len(failed),
        "passed_with_warnings": len(warned),
        "pass_rate": round(len(passed) / max(1, len(results)) * 100, 1),
        "blocked_files": [r["file"] for r in failed],
        "common_issues": _count_issues(failed),
    }

def _count_issues(failed_results: list) -> dict:
    from collections import Counter
    all_issues = [i.split(":")[0] for r in failed_results for i in r["issues"]]
    return dict(Counter(all_issues).most_common(10))
```

---

## Output

### Per-File Result

```json
{
  "file": "/Books-MD/science/class-6/chapter-04-magnets.md",
  "status": "PASS",
  "word_count": 2134,
  "formula_count": 0,
  "heading_count": 8,
  "issues": [],
  "warnings": [
    "NO_EXERCISE_MARKER: Could not find an exercise/activity section heading. Verify prose is not mixed with exercises."
  ],
  "frontmatter_parsed": {
    "grade": 6,
    "subject": "science",
    "chapter_number": 4,
    "chapter_title": "Fun with Magnets",
    "source": "NCERT"
  }
}
```

### Batch Report

```json
{
  "total": 48,
  "passed": 43,
  "failed": 5,
  "passed_with_warnings": 9,
  "pass_rate": 89.6,
  "blocked_files": [
    "/Books-MD/math/class-9/chapter-02-polynomials.md",
    "/Books-MD/science/class-7/chapter-05-acids-bases.md"
  ],
  "common_issues": {
    "MISSING_FRONTMATTER": 3,
    "HIGH_NON_ASCII": 2
  }
}
```

---

## Failure Recovery Guide

| Issue | Likely Cause | Fix |
|---|---|---|
| `MISSING_FRONTMATTER` | OCR output not post-processed | Re-run `pdf-to-markdown` Stage 0 post-processing script |
| `HIGH_NON_ASCII` | Multi-column layout OCR misread | Re-run OCR with `layout: "single-column"` hint |
| `REPEATED_CHARS` | Scan artefact (dots, lines) | Manually clean or re-scan source PDF |
| `TOO_SHORT` | Only part of chapter converted | Check if source PDF had multiple parts; merge or re-convert |
| `GRADE_MISMATCH` | File placed in wrong directory | Move file to correct grade folder; update frontmatter |
| `FEW_FORMULAS` (Math) | LaTeX not preserved | Re-run OCR with Mistral OCR math mode enabled |
| Semantic: `garbled` | Poor scan quality of original PDF | Source a better quality PDF; try alternative Mistral OCR settings |

---

## Quality Checks

- [ ] ≥ 95% of files in a batch pass automated structural checks before corpus ingestion
- [ ] Every FAIL file is re-processed or manually corrected before entering ARI corpus
- [ ] Batch validation report stored at `/ari/data/validation/md-validation-<date>.json`
- [ ] Spot-check at least 10% of PASS files with the AI semantic check
- [ ] Math chapters: verify formula count is plausible before excluding from prose corpus

## Notes
- Run validation immediately after every OCR batch — do not queue unchecked files into the content pipeline
- The NCERT word frequency list used by ARI is built from validated files only. Garbled text in the corpus directly corrupts the frequency rankings and degrades model quality.
- Store validation results alongside each MD file: `chapter-04-magnets.validation.json`
