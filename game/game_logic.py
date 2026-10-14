"""Pure game-logic helpers, intentionally independent of Pygame for testing."""
from __future__ import annotations
import random
import string

WORDS = ["PYTHON", "PYGAME", "PLANET", "ROCKET", "GALAXY", "STREAM", "PUZZLE", "ALGORITHM",
         "COMPUTER", "DEVELOPER", "FUNCTION", "VARIABLE", "KEYBOARD", "PIXEL", "CODING"]


def normalize_guess(value: str) -> str:
    """Normalize user input by trimming surrounding whitespace and uppercasing."""
    return (value or "").strip().upper()


def is_correct_guess(guess: str, secret_word: str) -> bool:
    """Compare against the secret target, never the scrambled display string."""
    normalized = normalize_guess(guess)
    return bool(normalized) and normalized == (secret_word or "").strip().upper()


def scramble_word(word: str, rng=None) -> str:
    """Return a permutation different from word when a different permutation exists."""
    rng = rng or random
    word = (word or "").upper()
    if len(word) <= 1 or len(set(word)) <= 1:
        return word
    letters = list(word)
    for _ in range(30):
        rng.shuffle(letters)
        result = "".join(letters)
        if result != word:
            return result
    # Deterministic fallback for pathological RNGs / repeated letters.
    for index in range(1, len(word)):
        result = word[index:] + word[:index]
        if result != word:
            return result
    return word


def reveal_next_hint(secret_word: str, revealed_positions: set[int]) -> tuple[set[int], str]:
    """Reveal the first still-hidden position; return a new set and display pattern."""
    secret = (secret_word or "").upper()
    updated = set(revealed_positions)
    next_position = next((i for i in range(len(secret)) if i not in updated), None)
    if next_position is not None:
        updated.add(next_position)
    pattern = " ".join(ch if i in updated else "_" for i, ch in enumerate(secret))
    return updated, pattern


def hinted_reward(base_points: int, hints_used: int) -> int:
    """Each hint reduces the round reward by one, with a minimum reward of zero."""
    return max(0, int(base_points) - max(0, int(hints_used)))


def valid_letter(value: str) -> bool:
    """True for a single alphabetic character accepted by the text box."""
    return len(value) == 1 and value in string.ascii_letters
