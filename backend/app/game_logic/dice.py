"""Dice rolling utilities.

The D20 system uses fair polyhedral dice where each face has an equal
probability of landing face up【171953677326081†L563-L566】. These helper
functions wrap Python's ``random`` module and provide convenience rolls for
common dice used in tabletop RPGs. All functions return integers.
"""

import random
from typing import List


def roll_die(sides: int) -> int:
    """Roll a die with the given number of sides and return the result.

    A fair die has a uniform probability distribution across all faces. The
    built‑in random number generator is used here for simplicity. In a
    production system you may wish to inject your own random source for
    reproducibility.
    """
    return random.randint(1, sides)


def roll_d4() -> int:
    return roll_die(4)


def roll_d6() -> int:
    return roll_die(6)


def roll_d8() -> int:
    return roll_die(8)


def roll_d10() -> int:
    return roll_die(10)


def roll_d12() -> int:
    return roll_die(12)


def roll_d20() -> int:
    return roll_die(20)


def roll_multiple(sides: int, count: int) -> List[int]:
    """Roll a die multiple times and return a list of results."""
    return [roll_die(sides) for _ in range(count)]
