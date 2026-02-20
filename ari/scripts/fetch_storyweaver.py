#!/usr/bin/env python3
"""
StoryWeaver Story Fetcher — Corpus Augmentation Step A3
Fetches Level 1–5 English stories from StoryWeaver using Playwright (real browser)
and saves them as Markdown files for ARI corpus augmentation.

Prerequisites:
    python3 -m pip install playwright
    python3 -m playwright install chromium

Usage:
    # Step 1 — Log in (one time, saves session):
    python3 ari/scripts/fetch_storyweaver.py --login

    # Step 2 — Fetch stories:
    python3 ari/scripts/fetch_storyweaver.py --level 1
    python3 ari/scripts/fetch_storyweaver.py --all

    # Single story test:
    python3 ari/scripts/fetch_storyweaver.py --url https://storyweaver.org.in/en/stories/369-the-red-raincoat

Output:
    ari/augmentation/storyweaver/level-{N}/story-{id}-{slug}.md
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_URL = "https://storyweaver.org.in"
NODE_API = f"{BASE_URL}/node/api/v1"
API_BASE = f"{BASE_URL}/api/v1"

# StoryWeaver Level → approximate CBSE grade
LEVEL_TO_GRADE = {1: 1, 2: 2, 3: 3, 4: 5, 5: 6}

OUTPUT_ROOT = Path("/Users/raghavrohatgi/Documents/AceQuest/ari/augmentation/storyweaver")
PROFILE_DIR = OUTPUT_ROOT / ".sw_profile"

MIN_WORD_COUNT = 30
TARGET_PER_LEVEL = 100
SLEEP_BETWEEN_STORIES = 1.2   # seconds — be polite


# ---------------------------------------------------------------------------
# Browser helpers
# ---------------------------------------------------------------------------

def make_context(pw, headed=False):
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    return pw.chromium.launch_persistent_context(
        str(PROFILE_DIR),
        headless=not headed,
        args=["--no-sandbox"],
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/144.0.0.0 Safari/537.36"
        ),
        locale="en-GB",
        viewport={"width": 1280, "height": 800},
    )


def browser_get_json(ctx, url: str) -> dict:
    """
    Navigate to a JSON API URL in the browser context and return parsed JSON.
    This works because the browser sends session cookies and bypasses Cloudflare.
    """
    p = ctx.new_page()
    try:
        try:
            p.goto(url, wait_until="domcontentloaded", timeout=20000)
        except Exception:
            pass
        time.sleep(1.5)
        body = p.evaluate("() => document.body.innerText")
        return json.loads(body)
    finally:
        p.close()


def has_session(ctx) -> bool:
    cookies = ctx.cookies()
    names = {c["name"] for c in cookies}
    return bool(names & {"_session_id", "_session"})


# ---------------------------------------------------------------------------
# API calls
# ---------------------------------------------------------------------------

def fetch_story_list(ctx, level: int, page: int = 1, per_page: int = 24) -> dict:
    """Fetch a listing page of English stories at a given level."""
    url = (f"{NODE_API}/books-search"
           f"?page={page}&per_page={per_page}"
           f"&levels[]={level}&languages[]=English&sort=New+Arrivals")
    return browser_get_json(ctx, url)


def fetch_story_read(ctx, slug: str) -> dict:
    """
    Fetch the full story content including all pages.
    Uses the /api/v1/stories/{slug}/read endpoint which returns HTML for each page.
    """
    url = f"{API_BASE}/stories/{slug}/read?story_pages=true&ignore_count=true"
    return browser_get_json(ctx, url)


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def extract_pages_text(pages: list) -> str:
    """
    Extract prose text from the pages list returned by the /read endpoint.
    Each page has an 'html' field with the page content.
    Skips cover pages and back-matter.
    """
    texts = []
    for page in pages:
        page_type = page.get("pageType", "")
        # Only take story pages (not covers/back-matter)
        if page_type not in ("StoryPage", ""):
            continue

        html = page.get("html") or page.get("content") or page.get("text") or ""
        if not html:
            continue

        # Strip HTML tags and script blocks first
        html_clean = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", html_clean)
        # Remove JS that appears as raw text in some pages:
        #   - $(document).ready(...)
        #   - var foo = ...
        #   - if(story_editor...)
        #   - function() { ... }
        text = re.sub(r"\$\(document\)[\s\S]*?\}\);", " ", text)
        text = re.sub(r"\bvar\s+\w+[\s\S]*?;", " ", text)
        text = re.sub(r"\bif\s*\(story_editor[\s\S]*?\}\s*\);?", " ", text)
        text = re.sub(r"story_editor\.[^;]+;", " ", text)
        text = re.sub(r"dictionary\.[^;]+;", " ", text)
        # Remove page number markers like "9/10"
        text = re.sub(r"\b\d+/\d+\b", "", text)
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text).strip()

        if text and len(text.split()) >= 3:
            texts.append(text)

    return "\n\n".join(texts)


# ---------------------------------------------------------------------------
# Markdown output
# ---------------------------------------------------------------------------

def to_markdown(story: dict, text: str, level: int) -> str:
    grade = LEVEL_TO_GRADE.get(level, level)
    title = story.get("name") or story.get("title") or "Unknown"
    story_id = story.get("id", 0)
    slug = story.get("slug", str(story_id))

    authors = story.get("authors", [])
    author_str = ", ".join(
        a.get("name", "") if isinstance(a, dict) else str(a)
        for a in (authors if isinstance(authors, list) else [])
    ).strip() or "Unknown"

    licence_raw = story.get("licence", {})
    licence = (licence_raw.get("name", "CC-BY 4.0")
               if isinstance(licence_raw, dict) else str(licence_raw) or "CC-BY 4.0")

    return "\n".join([
        "---",
        "source: StoryWeaver",
        f"level: {level}",
        f"grade: {grade}",
        "language: English",
        f"licence: {licence}",
        f"story_id: {story_id}",
        f'title: "{title}"',
        f'author: "{author_str}"',
        f"url: {BASE_URL}/en/stories/{slug}",
        "---",
        "",
        f"# {title}",
        "",
        text,
        "",
    ])


def save_story(story: dict, text: str, level: int) -> Path:
    story_id = story.get("id", 0)
    title = story.get("name") or story.get("title") or ""
    slug = story.get("slug", "")

    # Derive slug_part from slug (e.g. "369-the-red-raincoat" → "the-red-raincoat")
    if slug:
        # Remove leading numeric ID from slug
        slug_part = re.sub(r"^\d+-", "", slug)[:60]
    elif title:
        slug_part = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]
    else:
        slug_part = f"story-{story_id}"

    # Update title from slug if missing
    if not title and slug_part:
        title = slug_part.replace("-", " ").title()
        story = {**story, "name": title}

    out_dir = OUTPUT_ROOT / f"level-{level}"
    out_dir.mkdir(parents=True, exist_ok=True)

    path = out_dir / f"story-{story_id}-{slug_part}.md"
    path.write_text(to_markdown(story, text, level), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Fetch logic
# ---------------------------------------------------------------------------

def fetch_level(ctx, level: int, target: int = TARGET_PER_LEVEL) -> int:
    out_dir = OUTPUT_ROOT / f"level-{level}"
    out_dir.mkdir(parents=True, exist_ok=True)

    existing = set()
    for p in out_dir.glob("story-*.md"):
        m = re.search(r"story-(\d+)-", p.name)
        if m:
            existing.add(int(m.group(1)))

    print(f"\n{'='*55}")
    print(f"Level {level} → Grade {LEVEL_TO_GRADE.get(level, level)}  "
          f"(already have {len(existing)} stories)")
    print(f"{'='*55}")

    saved = 0
    skipped_short = 0
    page_num = 1
    total_available = None

    while saved < target:
        print(f"\n  Fetching listing page {page_num}...", end=" ", flush=True)

        try:
            data = fetch_story_list(ctx, level, page=page_num)
        except Exception as e:
            print(f"Error: {e}")
            break

        stories = data.get("data", data.get("stories", []))
        meta = data.get("meta", {})

        if total_available is None:
            total_available = meta.get("total", len(stories))
            print(f"({total_available} total available)")
        else:
            print(f"({len(stories)} on this page)")

        if not stories:
            print("  No more stories.")
            break

        for story in stories:
            story_id = story.get("id")
            story_slug = story.get("slug") or str(story_id)
            title = story.get("name") or story.get("title") or ""

            if not story_id or story_id in existing:
                continue

            print(f"    → {story_id}: '{title}'", end=" ", flush=True)
            time.sleep(SLEEP_BETWEEN_STORIES)

            try:
                read_data = fetch_story_read(ctx, story_slug)
            except Exception as e:
                print(f"✗ read error: {e}")
                existing.add(story_id)
                continue

            inner = read_data.get("data", read_data)
            pages = inner.get("pages", [])
            text = extract_pages_text(pages)
            word_count = len(text.split()) if text else 0

            if word_count < MIN_WORD_COUNT:
                skipped_short += 1
                existing.add(story_id)
                print(f"✗ too short ({word_count} words)")
                continue

            # Merge listing metadata with read metadata
            merged = {**story, **{k: v for k, v in inner.items() if k != "pages"}}
            path = save_story(merged, text, level)
            existing.add(story_id)
            saved += 1
            print(f"✓ {word_count} words → {path.name}")

            if saved >= target:
                break

        page_num += 1
        if page_num > 50:
            break

    print(f"\n  Level {level}: {saved} saved, {skipped_short} too short")
    return saved


def fetch_single(ctx, url: str) -> None:
    match = re.search(r"/stories/(\d+)-?([^/?]*)", url)
    if not match:
        print(f"Cannot parse story from URL: {url}")
        sys.exit(1)

    story_id = int(match.group(1))
    slug_part = match.group(2)
    slug = f"{story_id}-{slug_part}" if slug_part else str(story_id)

    print(f"Fetching story {story_id} ({slug})...")

    try:
        read_data = fetch_story_read(ctx, slug)
    except Exception as e:
        print(f"Error fetching /read: {e}")
        sys.exit(1)

    inner = read_data.get("data", read_data)
    # Ensure id and slug are set (read response may not include them directly)
    if not inner.get("id"):
        inner["id"] = story_id
    if not inner.get("slug"):
        inner["slug"] = slug

    pages = inner.get("pages", [])
    text = extract_pages_text(pages)

    level_raw = inner.get("level", 1)
    try:
        level = int(level_raw)
    except (ValueError, TypeError):
        level = 1

    if not text:
        print(f"No text extracted. Pages: {len(pages)}")
        print("Page types:", [p.get("pageType") for p in pages[:5]])
        return

    path = save_story(inner, text, level)
    print(f"Saved: {path}")
    print(f"Level: {level} → Grade: {LEVEL_TO_GRADE.get(level, level)}")
    print(f"Word count: {len(text.split())}")
    print(f"\nText preview:\n{text[:500]}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fetch StoryWeaver stories for ARI corpus augmentation"
    )
    parser.add_argument("--level", type=int, choices=[1, 2, 3, 4, 5])
    parser.add_argument("--all", action="store_true", help="Fetch levels 1–5")
    parser.add_argument("--url", type=str, help="Fetch a single story by URL")
    parser.add_argument("--login", action="store_true",
                        help="Open browser to log in (first-time setup)")
    parser.add_argument("--headed", action="store_true",
                        help="Show browser window")
    parser.add_argument("--target", type=int, default=TARGET_PER_LEVEL,
                        help=f"Stories per level (default: {TARGET_PER_LEVEL})")
    args = parser.parse_args()

    if not any([args.level, args.all, args.url, args.login]):
        parser.print_help()
        print("\nStep 1 (first time): python3 ari/scripts/fetch_storyweaver.py --login")
        print("Step 2:              python3 ari/scripts/fetch_storyweaver.py --level 1")
        sys.exit(1)

    from playwright.sync_api import sync_playwright

    print("=== StoryWeaver Fetcher ===")
    print(f"Output: {OUTPUT_ROOT}")

    # Always run headed — StoryWeaver's Cloudflare protection blocks headless browsers
    use_headed = True

    with sync_playwright() as pw:
        ctx = make_context(pw, headed=use_headed)

        if args.login:
            print("\nOpening browser for login...")
            print("Log in to StoryWeaver, then press Ctrl+C here.")
            p = ctx.new_page()
            try:
                p.goto(f"{BASE_URL}/en/sign-in",
                       wait_until="domcontentloaded", timeout=15000)
            except Exception:
                pass
            try:
                time.sleep(180)
            except KeyboardInterrupt:
                pass
            p.close()
            ctx.close()
            print("Session saved. Run without --login to fetch stories.")
            return

        if not has_session(ctx):
            print("No session found. Run: python3 ari/scripts/fetch_storyweaver.py --login")
            ctx.close()
            sys.exit(1)

        print("Session cookies present ✓")

        try:
            if args.url:
                fetch_single(ctx, args.url)
            else:
                levels = [1, 2, 3, 4, 5] if args.all else [args.level]
                total = sum(fetch_level(ctx, lv, args.target) for lv in levels)
                print(f"\n=== Done: {total} stories saved to {OUTPUT_ROOT} ===")
        finally:
            ctx.close()


if __name__ == "__main__":
    main()
