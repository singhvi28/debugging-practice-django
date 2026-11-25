"""Subtractive jitter for retry delays."""

import random


def apply_jitter(base_ms: float, jitter_ms: int, seed: int | None = None) -> float:
    """Subtract random jitter from the base delay."""
    rng = random.Random(seed)
    return base_ms - rng.randint(0, jitter_ms)
