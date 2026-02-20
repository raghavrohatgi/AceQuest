# Skill: readability-check

## Purpose
Calculate the Flesch-Kincaid grade level of a text passage and verify it's appropriate for the target grade. Used primarily for English comprehension passages before questions are generated against them.

## Used By
- English Teacher agents (via `generate-passage` skill)
- QA Reviewer Agent (Stage 3, for English passages)

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `text` | string | The passage text to evaluate |
| `target_grade` | integer | The intended grade level |
| `tolerance` | integer | Acceptable grade level variance (default: ±1) |

## Procedure

### Step 1: Calculate Flesch-Kincaid Grade Level

```python
import re

def syllable_count(word: str) -> int:
    """Approximate syllable counter for English words."""
    word = word.lower().strip(".,!?;:'\"")
    if len(word) <= 3:
        return 1
    # Count vowel groups
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    # Adjust for silent e
    if word.endswith("e"):
        count -= 1
    return max(1, count)

def flesch_kincaid_grade(text: str) -> float:
    """Returns Flesch-Kincaid Grade Level."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = re.findall(r'\b[a-zA-Z]+\b', text)

    if not sentences or not words:
        return 0.0

    total_sentences = len(sentences)
    total_words = len(words)
    total_syllables = sum(syllable_count(w) for w in words)

    asl = total_words / total_sentences          # Average Sentence Length
    asw = total_syllables / total_words          # Average Syllables per Word

    fk_grade = (0.39 * asl) + (11.8 * asw) - 15.59
    return round(fk_grade, 1)

def check_readability(text: str, target_grade: int, tolerance: int = 1) -> dict:
    fk = flesch_kincaid_grade(text)
    word_count = len(re.findall(r'\b[a-zA-Z]+\b', text))
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    avg_sentence_length = round(word_count / len(sentences), 1) if sentences else 0

    in_range = (target_grade - tolerance) <= fk <= (target_grade + tolerance)

    return {
        "flesch_kincaid_grade": fk,
        "target_grade": target_grade,
        "tolerance": tolerance,
        "in_range": in_range,
        "word_count": word_count,
        "sentence_count": len(sentences),
        "avg_sentence_length": avg_sentence_length,
        "status": "PASS" if in_range else "NEEDS_REVISION",
        "adjustment_needed": (
            "shorten_sentences_and_simplify_vocabulary" if fk > target_grade + tolerance
            else "lengthen_sentences_or_add_complexity" if fk < target_grade - tolerance
            else None
        )
    }
```

### Step 2: If NEEDS_REVISION

If `status == "NEEDS_REVISION"`, send a revision prompt to the English agent:

**Too complex (FK > target + tolerance):**
```
The passage has a Flesch-Kincaid grade level of {fk}, but the target is Grade {target} (±1).
It is too complex. Please revise the passage to:
- Shorten sentences to an average of ≤ {max_sentence_length} words
- Replace complex vocabulary with simpler alternatives
- Break compound sentences into shorter ones
Keep the same theme and content. Do not change facts or meaning.
Return the revised passage only.
```

**Too simple (FK < target - tolerance):**
```
The passage has a Flesch-Kincaid grade level of {fk}, but the target is Grade {target} (±1).
It is too simple. Please revise the passage to:
- Use slightly longer sentences where natural
- Introduce 2-3 grade-appropriate vocabulary words
- Add more descriptive detail
Keep the same theme and content. Do not change facts or meaning.
Return the revised passage only.
```

## Output

```json
{
  "passage_id": "eng-6-passage-001",
  "text_preview": "Water is essential for all living things...",
  "flesch_kincaid_grade": 5.8,
  "target_grade": 6,
  "tolerance": 1,
  "in_range": true,
  "word_count": 182,
  "sentence_count": 14,
  "avg_sentence_length": 13.0,
  "status": "PASS",
  "adjustment_needed": null
}
```

## Grade-Band Reference

| Grade | FK Target | Max Avg Sentence Length | Vocabulary Level |
| --- | --- | --- | --- |
| 1 | 1.0 | 6 words | CVC words, sight words |
| 2 | 2.0 | 8 words | Common 100-word vocabulary |
| 3 | 3.0 | 10 words | 500 most common words |
| 4 | 4.0 | 12 words | Grade 4 word lists |
| 5 | 5.0 | 13 words | Grade 5 word lists |
| 6 | 6.0 | 15 words | Standard informational |
| 7 | 7.0 | 17 words | Academic vocabulary |
| 8 | 8.0 | 18 words | Advanced informational |
| 9 | 9.0 | 20 words | Formal register |
| 10 | 10.0 | 22 words | Near-adult register |

## Quality Checks

- [ ] All passages have `flesch_kincaid_grade` recorded in the passage JSON
- [ ] All passages pass before questions are generated against them
- [ ] Maximum 2 revision rounds — if still failing, flag for manual edit

## Notes
- FK grade is an approximation — always do a sanity-check read of the passage yourself. A Grade 6 student should be able to read it comfortably without stopping more than once.
- Hindi proper nouns in the passage will distort the syllable count slightly. This is acceptable.
- Very short passages (< 50 words) will have unreliable FK scores — use judgment for Grade 1-2 content.
