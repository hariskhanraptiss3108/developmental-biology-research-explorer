"""Small statistics helpers written with plain Python so beginners can read them.

We use PERMUTATION tests: they ask "if the group labels were meaningless, how often would
shuffling them give a difference at least as large as the one we saw?"
Assumptions (also shown in the app):
  * Observations are independent (one value per animal/well/specimen, not repeated measures
    of the same one unless using the paired test).
  * Under the "no difference" idea, labels can be shuffled (e.g. units were allocated at random).
  * It does not assume a bell-shaped (normal) distribution.
It says nothing about whether a difference is biologically important, and small samples
can only provide weak evidence.
"""
from __future__ import annotations

import math
import random


def _check(values, name: str, minimum: int = 2) -> list[float]:
    cleaned = [float(v) for v in values]
    if len(cleaned) < minimum:
        raise ValueError(f"{name} needs at least {minimum} values (got {len(cleaned)}).")
    if any(math.isnan(v) for v in cleaned):
        raise ValueError(f"{name} contains missing (NaN) values.")
    return cleaned


def mean(values) -> float:
    vals = _check(values, "Data", minimum=1)
    return sum(vals) / len(vals)


def sample_sd(values) -> float:
    """Sample standard deviation (divides by n - 1)."""
    vals = _check(values, "Data", minimum=2)
    m = sum(vals) / len(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))


def cohens_d(group_a, group_b) -> float:
    """Standardised difference between means (pooled SD). Returns 0.0 if both groups have no spread and equal means."""
    a, b = _check(group_a, "Group A"), _check(group_b, "Group B")
    pooled_var = ((len(a) - 1) * sample_sd(a) ** 2 + (len(b) - 1) * sample_sd(b) ** 2) / (len(a) + len(b) - 2)
    diff = mean(a) - mean(b)
    if pooled_var == 0:
        return 0.0 if diff == 0 else math.inf
    return diff / math.sqrt(pooled_var)


def permutation_test_independent(group_a, group_b, n_permutations: int = 10000, seed: int = 42) -> dict:
    """Two-sided permutation test for a difference in means between two separate groups."""
    a, b = _check(group_a, "Group A"), _check(group_b, "Group B")
    if n_permutations < 100:
        raise ValueError("Use at least 100 permutations.")
    observed = mean(a) - mean(b)
    pooled = a + b
    rng = random.Random(seed)
    as_extreme = 0
    for _ in range(n_permutations):
        rng.shuffle(pooled)
        diff = mean(pooled[:len(a)]) - mean(pooled[len(a):])
        if abs(diff) >= abs(observed) - 1e-12:
            as_extreme += 1
    # +1 on both sides so the p-value can never be exactly zero
    return {"observed_difference": observed, "p_value": (as_extreme + 1) / (n_permutations + 1),
            "n_permutations": n_permutations}


def paired_sign_flip_test(before, after, n_permutations: int = 10000, seed: int = 42) -> dict:
    """Two-sided test for paired data (same subjects measured twice).

    Under "no change", the sign of each subject's difference is arbitrary, so we randomly flip signs.
    """
    x, y = _check(before, "Before"), _check(after, "After")
    if len(x) != len(y):
        raise ValueError("Paired data need the same number of measurements at both time points.")
    differences = [late - early for early, late in zip(x, y)]
    observed = mean(differences)
    rng = random.Random(seed)
    as_extreme = 0
    for _ in range(n_permutations):
        flipped = [d if rng.random() < 0.5 else -d for d in differences]
        if abs(mean(flipped)) >= abs(observed) - 1e-12:
            as_extreme += 1
    return {"observed_difference": observed, "p_value": (as_extreme + 1) / (n_permutations + 1),
            "n_permutations": n_permutations, "n_pairs": len(differences)}
