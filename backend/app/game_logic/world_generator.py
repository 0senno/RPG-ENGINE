"""Procedural world generation utilities.

This module can generate a new campaign world given a random seed. It creates
a square grid of locations with different terrain types, spawns a handful of
NPCs and seeds a simple quest. Worlds are stored in the database via the
Location and NPC models. You can adjust the WORLD_SIZE, terrain frequencies and
NPC archetypes to suit your game.
"""

import random
from typing import List, Tuple

from sqlalchemy.orm import Session

from .. import models


WORLD_SIZE = 20  # 20x20 grid
TERRAINS = ["plains", "forest", "mountain", "water", "desert"]

NPC_ARCHETYPES = [
    {"name": "Grimwald", "kindness": -0.7, "greed": 0.3, "curiosity": -0.2},
    {"name": "Seraphina", "kindness": 0.8, "greed": -0.5, "curiosity": 0.4},
    {"name": "Rattlebones", "kindness": -0.4, "greed": 0.7, "curiosity": 0.1},
    {"name": "Lilypad", "kindness": 0.2, "greed": -0.3, "curiosity": 0.9},
]


def generate_world(db: Session, seed: int = None) -> None:
    """Populate the database with a new world based on a seed.

    Existing data in the Location and NPC tables will be cleared. Pass a seed
    to get deterministic worlds for reproducible campaigns.
    """
    if seed is not None:
        random.seed(seed)

    # Clear existing locations and NPCs
    db.query(models.NPC).delete()
    db.query(models.Location).delete()
    db.commit()

    # Create grid of locations
    for x in range(WORLD_SIZE):
        for y in range(WORLD_SIZE):
            terrain = random.choice(TERRAINS)
            loc = models.Location(x=x, y=y, terrain=terrain, discovered=False)
            db.add(loc)
    db.commit()

    # Spawn NPCs at random positions
    for arch in NPC_ARCHETYPES:
        npc = models.NPC(
            name=arch["name"],
            kindness=arch["kindness"],
            greed=arch["greed"],
            curiosity=arch["curiosity"],
        )
        # Pick a random location
        npc.x = random.randint(0, WORLD_SIZE - 1)
        npc.y = random.randint(0, WORLD_SIZE - 1)
        db.add(npc)
    db.commit()
