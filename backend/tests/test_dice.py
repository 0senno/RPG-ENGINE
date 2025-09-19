"""Tests for dice fairness.

These tests ensure that the d20 produces an approximately uniform distribution
of results. Because randomness is involved the threshold is deliberately
loose; if this test fails consistently you may need to increase the sample
size or adjust the tolerance. The uniform nature of fair dice comes from
their face‑transitive symmetry【171953677326081†L563-L566】.
"""

import statistics
from collections import Counter

from app.game_logic.dice import roll_d20


def test_d20_distribution():
    rolls = [roll_d20() for _ in range(10000)]
    counts = Counter(rolls)
    # Expect roughly 500 occurrences per face (10000/20)
    expected = len(rolls) / 20
    # Standard deviation for binomial distribution
    # p = 1/20, n = 10000 => std = sqrt(n * p * (1-p))
    import math

    std = math.sqrt(len(rolls) * (1 / 20) * (19 / 20))
    for face in range(1, 21):
        assert abs(counts[face] - expected) < 4 * std, f"Face {face} frequency deviates too much"
