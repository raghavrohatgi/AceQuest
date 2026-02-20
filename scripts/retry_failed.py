#!/usr/bin/env python3
"""Retry only the failed files from a previous pdf_to_markdown.py batch run."""
import json
import sys
import time
from pathlib import Path

# Add scripts dir to path so we can import the main script's functions
sys.path.insert(0, str(Path(__file__).parent))
from pdf_to_markdown import convert_pdf, OUTPUT_DIR

log_path = OUTPUT_DIR / "_conversion_log.json"
data = json.loads(log_path.read_text())

failed = [r for r in data if r.get("status") == "error"]
print(f"Retrying {len(failed)} failed files (with 10s initial wait for API stability)...\n")
time.sleep(10)

results_map = {r["path"]: r for r in data}

success = errors = 0
for i, record in enumerate(failed, 1):
    pdf_path = Path(record["path"])
    print(f"[{i}/{len(failed)}]", end=" ")
    result = convert_pdf(pdf_path)
    results_map[record["path"]] = result

    if result["status"] == "success":
        success += 1
    else:
        errors += 1

    # Save updated log after each file
    log_path.write_text(json.dumps(list(results_map.values()), indent=2))

    if result["status"] == "success":
        time.sleep(1)  # gentle pacing after success

print(f"\n=== RETRY COMPLETE ===")
print(f"  Recovered: {success}")
print(f"  Still failing: {errors}")
