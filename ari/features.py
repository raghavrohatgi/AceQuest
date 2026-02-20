"""
ARI Feature Extractor — Phase 2.1 (extended)
Computes readability features from a text string against the NCERT corpus.

Features:
  1. mean_word_frequency_rank  — avg NCERT corpus rank of content words (lower = more common)
  2. mean_sentence_length      — avg tokens per sentence
  3. type_token_ratio          — unique words / total words (vocabulary diversity)
  4. avg_syllables_per_word    — proxy for word complexity (via pyphen)
  5. pct_rare_words            — % words not in top-500 familiar vocab for the target grade
  6. mean_log_freq_rank        — log-scale frequency rank (reduces outlier effect)
  7. lexical_density           — content words / all non-punct tokens
  8. flesch_kincaid_grade      — FK Grade Level (0.39*ASL + 11.8*ASW - 15.59)
  9. gunning_fog               — 0.4 * (ASL + % 3-syllable complex words)
 10. sentence_length_variance  — variance of per-sentence word counts
 11. subordinate_clause_ratio  — subordinating conjunctions per sentence
 12. long_word_ratio           — fraction of content words with 3+ syllables

Usage:
    from ari.features import FeatureExtractor
    fe = FeatureExtractor()
    features = fe.extract("The magnet attracts iron filings.", grade=6)
    # → {"mean_word_frequency_rank": 4820.3, "mean_sentence_length": 5.0, ...}
"""

import json
import re
import string
from functools import lru_cache
from pathlib import Path

import math
import nltk
import pyphen

# --- NLTK bootstrap ---
for _pkg, _path in [("punkt_tab", "tokenizers/punkt_tab"), ("punkt", "tokenizers/punkt")]:
    try:
        nltk.data.find(_path)
    except LookupError:
        nltk.download(_pkg, quiet=True)

from nltk.tokenize import sent_tokenize, word_tokenize

# --- Data paths ---
DATA_DIR = Path(__file__).parent / "data"
FREQ_FILE = DATA_DIR / "ncert-word-frequency.json"
VOCAB_FILE = DATA_DIR / "grade-vocab-lists.json"
VOCAB_SUBJECT_FILE = DATA_DIR / "grade-subject-vocab-lists.json"

# --- Module-level singletons (loaded once, reused across calls) ---
_freq_rank: dict[str, int] = {}              # word → rank (1 = most common)
_grade_vocab: dict[str, set[str]] = {}       # "6" → set of familiar words
_grade_subject_vocab: dict[str, set[str]] = {}  # "6_Science" → set of familiar words
_dic = pyphen.Pyphen(lang="en_GB")     # British English closest to Indian English

# Punctuation set for fast filtering
_PUNCT = set(string.punctuation)
_RE_ALPHA = re.compile(r"^[a-zA-Z][a-zA-Z\-']*[a-zA-Z]$|^[a-zA-Z]$")
_FALLBACK_RANK = 20_000  # rank assigned to words not in NCERT corpus (very rare)

# Subordinating conjunctions (signal complex/compound sentences)
_SUBORD_CONJ = {
    "although", "because", "since", "while", "whereas", "unless", "until",
    "though", "even", "if", "when", "whenever", "wherever", "after", "before",
    "once", "whether", "that", "which", "who", "whom", "whose", "as",
}


def _load_data() -> None:
    """Load frequency and vocab data into module-level dicts (idempotent)."""
    global _freq_rank, _grade_vocab

    if _freq_rank and _grade_vocab:
        return  # already loaded

    if not FREQ_FILE.exists():
        raise FileNotFoundError(
            f"NCERT frequency file not found: {FREQ_FILE}\n"
            "Run ari/scripts/build_frequency_list.py first."
        )
    if not VOCAB_FILE.exists():
        raise FileNotFoundError(
            f"Grade vocab file not found: {VOCAB_FILE}\n"
            "Run ari/scripts/build_vocab_lists.py first."
        )

    freq_list = json.loads(FREQ_FILE.read_text(encoding="utf-8"))
    _freq_rank = {item["word"]: item["rank"] for item in freq_list}

    vocab_raw = json.loads(VOCAB_FILE.read_text(encoding="utf-8"))
    _grade_vocab = {grade: set(words) for grade, words in vocab_raw.items()}

    # Load per-grade-subject vocab if available (more precise rare-word signal)
    if VOCAB_SUBJECT_FILE.exists():
        vocab_subj_raw = json.loads(VOCAB_SUBJECT_FILE.read_text(encoding="utf-8"))
        _grade_subject_vocab.update({k: set(v) for k, v in vocab_subj_raw.items()})


def _is_content_token(token: str) -> bool:
    """Return True if this token is a scoreable content word."""
    t = token.lower()
    return bool(_RE_ALPHA.match(t)) and len(t) >= 2


def _syllable_count(word: str) -> int:
    """Count syllables in a word using pyphen. Fallback: count vowel groups."""
    word = word.lower()
    # pyphen returns hyphenated word; count segments
    hyphenated = _dic.inserted(word)
    if hyphenated:
        count = hyphenated.count("-") + 1
        return max(1, count)
    # Fallback: count vowel clusters
    vowels = re.findall(r"[aeiou]+", word)
    return max(1, len(vowels))


def _closest_grade_vocab(grade: int, subject: str = "") -> set[str]:
    """Return the familiar vocabulary set for the given grade and subject.
    Prefers per-grade-subject vocab; falls back to per-grade."""
    g = str(max(1, min(10, grade)))
    if subject:
        key = f"{g}_{subject}"
        if key in _grade_subject_vocab:
            return _grade_subject_vocab[key]
    return _grade_vocab.get(g, set())


class FeatureExtractor:
    """
    Extracts ARI readability features from a text string.

    Parameters
    ----------
    None — data is loaded from /ari/data/ automatically on first call.
    """

    def __init__(self) -> None:
        _load_data()

    def extract(self, text: str, grade: int, subject: str = "") -> dict:
        """
        Compute ARI features for a text at a given target grade.

        Parameters
        ----------
        text    : str  — The passage to score (ideally 20+ words)
        grade   : int  — CBSE class level (1–10); used for pct_rare_words baseline
        subject : str  — "English", "Maths", or "Science" (optional, improves rare-word signal)

        Returns
        -------
        dict with keys:
            mean_word_frequency_rank  (float)  — lower = more common words
            mean_sentence_length      (float)  — avg words per sentence
            type_token_ratio          (float)  — 0.0–1.0
            avg_syllables_per_word    (float)  — avg syllables per content word
            pct_rare_words            (float)  — 0.0–100.0
            word_count                (int)    — total content words
            sentence_count            (int)    — total sentences
        """
        if not text or not text.strip():
            return self._zero_features()

        # --- Sentence tokenisation ---
        sentences = sent_tokenize(text)
        sentence_count = len(sentences)

        # --- Word tokenisation ---
        all_tokens = word_tokenize(text.lower())
        content_tokens = [t for t in all_tokens if _is_content_token(t)]
        word_count = len(content_tokens)

        if word_count == 0:
            return self._zero_features()

        # --- Feature 1: Mean word frequency rank ---
        ranks = [_freq_rank.get(t, _FALLBACK_RANK) for t in content_tokens]
        mean_word_frequency_rank = sum(ranks) / len(ranks)

        # --- Feature 2: Mean sentence length (in tokens) ---
        # Count tokens per sentence (content words only per sentence)
        sent_lengths = []
        for sent in sentences:
            toks = word_tokenize(sent.lower())
            content_toks = [t for t in toks if _is_content_token(t)]
            sent_lengths.append(len(content_toks))
        mean_sentence_length = sum(sent_lengths) / max(1, len(sent_lengths))

        # --- Feature 3: Type-Token Ratio ---
        unique_words = set(content_tokens)
        type_token_ratio = len(unique_words) / word_count

        # --- Feature 4: Average syllables per word ---
        syllable_counts = [_syllable_count(t) for t in content_tokens]
        avg_syllables_per_word = sum(syllable_counts) / len(syllable_counts)

        # --- Feature 5: % rare words (not in familiar vocab for this grade/subject) ---
        familiar = _closest_grade_vocab(grade, subject)
        rare_words = [t for t in content_tokens if t not in familiar]
        pct_rare_words = (len(rare_words) / word_count) * 100.0

        # --- Feature 6: Mean log frequency rank (log-scale reduces outlier effect) ---
        log_ranks = [math.log1p(_freq_rank.get(t, _FALLBACK_RANK)) for t in content_tokens]
        mean_log_freq_rank = sum(log_ranks) / len(log_ranks)

        # --- Feature 7: Lexical density — content words / all non-punct tokens ---
        all_word_tokens = [t for t in all_tokens if t not in _PUNCT and t.strip()]
        lexical_density = word_count / max(1, len(all_word_tokens))

        # --- Feature 8: Flesch-Kincaid Grade Level ---
        # FK GL = 0.39 * ASL + 11.8 * ASW - 15.59
        # ASL = avg sentence length (all tokens), ASW = avg syllables per word
        asl = len(all_word_tokens) / max(1, sentence_count)
        flesch_kincaid_grade = round(0.39 * asl + 11.8 * avg_syllables_per_word - 15.59, 3)

        # --- Feature 9: Gunning Fog Index ---
        # Fog = 0.4 * (ASL + % words with 3+ syllables)
        complex_word_count = sum(1 for s in syllable_counts if s >= 3)
        pct_complex = (complex_word_count / word_count) * 100.0
        gunning_fog = round(0.4 * (mean_sentence_length + pct_complex), 3)

        # --- Feature 10: Sentence length variance ---
        mean_sl = sum(sent_lengths) / max(1, len(sent_lengths))
        sent_length_variance = sum((l - mean_sl) ** 2 for l in sent_lengths) / max(1, len(sent_lengths))

        # --- Feature 11: Subordinate clause ratio (conjunctions per sentence) ---
        all_tokens_lower = [t.lower() for t in all_tokens]
        subord_count = sum(1 for t in all_tokens_lower if t in _SUBORD_CONJ)
        subordinate_clause_ratio = round(subord_count / max(1, sentence_count), 4)

        # --- Feature 12: Long word ratio (3+ syllable content words) ---
        long_word_ratio = round(complex_word_count / word_count, 4)

        return {
            "mean_word_frequency_rank": round(mean_word_frequency_rank, 2),
            "mean_sentence_length": round(mean_sentence_length, 2),
            "type_token_ratio": round(type_token_ratio, 4),
            "avg_syllables_per_word": round(avg_syllables_per_word, 4),
            "pct_rare_words": round(pct_rare_words, 2),
            "mean_log_freq_rank": round(mean_log_freq_rank, 4),
            "lexical_density": round(lexical_density, 4),
            "flesch_kincaid_grade": flesch_kincaid_grade,
            "gunning_fog": gunning_fog,
            "sentence_length_variance": round(sent_length_variance, 4),
            "subordinate_clause_ratio": subordinate_clause_ratio,
            "long_word_ratio": long_word_ratio,
            "word_count": word_count,
            "sentence_count": sentence_count,
        }

    def _zero_features(self) -> dict:
        return {
            "mean_word_frequency_rank": 0.0,
            "mean_sentence_length": 0.0,
            "type_token_ratio": 0.0,
            "avg_syllables_per_word": 0.0,
            "pct_rare_words": 0.0,
            "mean_log_freq_rank": 0.0,
            "lexical_density": 0.0,
            "flesch_kincaid_grade": 0.0,
            "gunning_fog": 0.0,
            "sentence_length_variance": 0.0,
            "subordinate_clause_ratio": 0.0,
            "long_word_ratio": 0.0,
            "word_count": 0,
            "sentence_count": 0,
        }


# ---------------------------------------------------------------------------
# Quick self-test — run: python3 -m ari.features
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    fe = FeatureExtractor()

    TEST_PASSAGES = [
        (1, "The cat sat on the mat. One bird and two fish."),
        (3, "The children played in the garden with their friends. They saw many birds and flowers."),
        (6, "Photosynthesis is the process by which plants make their own food using sunlight, water, and carbon dioxide."),
        (9, "The acceleration of a body is directly proportional to the net force applied and inversely proportional to its mass."),
        (10, "The concept of entropy in thermodynamics describes the degree of disorder or randomness in a closed system."),
    ]

    print("=== FeatureExtractor Self-Test ===\n")
    print(f"{'Grade':<7} {'FreqRank':>10} {'SentLen':>9} {'TTR':>7} {'Sylls':>7} {'Rare%':>7} {'Words':>6}")
    print("-" * 60)
    for grade, text in TEST_PASSAGES:
        f = fe.extract(text, grade)
        print(
            f"Gr {grade:<4} "
            f"{f['mean_word_frequency_rank']:>10.1f} "
            f"{f['mean_sentence_length']:>9.1f} "
            f"{f['type_token_ratio']:>7.3f} "
            f"{f['avg_syllables_per_word']:>7.3f} "
            f"{f['pct_rare_words']:>7.1f} "
            f"{f['word_count']:>6}"
        )

    print("\nExpected trends:")
    print("  FreqRank    → should INCREASE with grade (harder words = higher rank)")
    print("  SentLen     → should INCREASE with grade")
    print("  TTR         → roughly stable or increasing")
    print("  Sylls       → should INCREASE with grade")
    print("  Rare%       → should INCREASE with grade (harder vocab vs. familiar list)")
