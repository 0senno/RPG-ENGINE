"""Simple NPC agent loop.

The NPCAgent class simulates basic behaviours for non‑player characters. On
each tick it observes its surroundings, decides on an action based on its
personality matrix and then performs that action. The actions implemented
here are simplistic: speak, move randomly, trade (no actual inventory
exchange), attack the player, or do nothing.

This module does not use asynchronous loops because it is run on demand by
the backend when an endpoint requests an NPC update. In a real game you
would run agents in background tasks or using websockets to push updates.
"""

import random
from typing import Optional, Tuple, List

from sqlalchemy.orm import Session

from . import models, crud
from .game_logic.dice import roll_d20


class NPCAgent:
    def __init__(self, npc: models.NPC, db: Session):
        self.npc = npc
        self.db = db

    def observe(self) -> dict:
        """Observe the immediate surroundings: adjacent players or NPCs.

        This simplified version checks for players at the same location. It
        could be extended to look within a radius or line of sight.
        """
        players_here = (
            self.db.query(models.Player)
            .filter(models.Player.x == self.npc.x, models.Player.y == self.npc.y)
            .all()
        )
        return {"players": players_here}

    def decide(self, observation: dict) -> str:
        """Decide on an action based on personality and observation.

        The decision logic uses the personality axes to weight possible actions.
        For instance, a hostile (low kindness) NPC is more likely to attack,
        whereas a curious NPC might initiate dialogue. The output is a string
        representing the chosen action.
        """
        kindness = self.npc.kindness
        greed = self.npc.greed
        curiosity = self.npc.curiosity
        players_here = observation.get("players", [])

        actions = []
        # Attack probability increases when players are present and kindness is low
        if players_here and kindness < -0.3:
            actions.append("attack")
        # Talk if curious and players are present
        if players_here and curiosity > 0.0:
            actions.append("talk")
        # Wander randomly if no other drives
        actions.append("wander")
        # Trade if greed is low (generous) and player present
        if players_here and greed < -0.2:
            actions.append("trade")

        return random.choice(actions)

    def act(self, action: str) -> Optional[str]:
        """Perform the chosen action. Returns a message describing the action.
        """
        if action == "attack":
            return self._attack()
        if action == "talk":
            return self._talk()
        if action == "trade":
            return self._trade()
        if action == "wander":
            return self._wander()
        return None

    def _attack(self) -> str:
        """Attack the first player at the NPC's location."""
        players_here = (
            self.db.query(models.Player)
            .filter(models.Player.x == self.npc.x, models.Player.y == self.npc.y)
            .all()
        )
        if not players_here:
            return f"{self.npc.name} looks around but finds no one to attack."
        player = players_here[0]
        attack_roll = roll_d20()
        damage = random.randint(1, 6)
        player.hp -= damage
        self.db.commit()
        return (
            f"{self.npc.name} attacks {player.name}! (roll {attack_roll}) "
            f"dealing {damage} damage."
        )

    def _talk(self) -> str:
        """Return a simple dialogue line based on personality."""
        # Very simple dialogue generator. You can replace this with an LLM.
        if self.npc.kindness > 0.5:
            line = "Greetings, traveller. The weather is nice today, isn't it?"
        elif self.npc.kindness < -0.5:
            line = "Get lost. I don't trust strangers."
        else:
            line = "What brings you to these parts?"
        return f"{self.npc.name} says: '{line}'"

    def _trade(self) -> str:
        return f"{self.npc.name} offers to trade, but real trading isn't implemented yet."

    def _wander(self) -> str:
        """Move one step in a random direction."""
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.npc.x += dx
        self.npc.y += dy
        self.db.commit()
        return f"{self.npc.name} wanders to ({self.npc.x}, {self.npc.y})."

    def tick(self) -> Optional[str]:
        """Run a single observe‑decide‑act loop and return the action message."""
        obs = self.observe()
        action = self.decide(obs)
        message = self.act(action)
        return message
