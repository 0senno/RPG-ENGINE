"""Simple turn‑based combat engine.

This module implements a rudimentary combat system inspired by tabletop RPGs.
Participants roll for initiative using a d20; the highest result acts first and
order remains fixed for the duration of the encounter. On their turn
characters may attack a target. Damage is determined by rolling a weapon
damage die (default d6 for all combatants). Critical hits occur on natural 20s
and double the damage.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import random

from ..models import Player, NPC
from .dice import roll_d20, roll_d6


@dataclass
class Combatant:
    """Container for combatant statistics used during an encounter."""

    name: str
    hp: int
    is_player: bool
    entity: object  # underlying Player or NPC object
    initiative: int = 0


class CombatEncounter:
    """Manages a single combat encounter between players and NPCs."""

    def __init__(self, participants: List[Combatant]):
        self.participants = participants
        self.round_order: List[Combatant] = []
        self.current_index = 0
        self.active = True
        self._roll_initiative()

    def _roll_initiative(self):
        """Determine initiative order by rolling a d20 for each participant."""
        for c in self.participants:
            c.initiative = roll_d20()
        self.participants.sort(key=lambda c: c.initiative, reverse=True)
        self.round_order = self.participants.copy()

    def next_turn(self) -> Optional[Tuple[Combatant, str]]:
        """Advance to the next combatant's turn and perform a basic attack.

        Returns a tuple of the combatant and a message describing the action.
        If the encounter is over (all enemies or players are down), returns None.
        """
        # Check if combat is over
        alive_players = [c for c in self.participants if c.is_player and c.hp > 0]
        alive_npcs = [c for c in self.participants if not c.is_player and c.hp > 0]
        if not alive_players or not alive_npcs:
            self.active = False
            return None

        combatant = self.round_order[self.current_index]
        # Skip dead combatants
        if combatant.hp <= 0:
            self.current_index = (self.current_index + 1) % len(self.round_order)
            return self.next_turn()

        # Determine target: pick first alive opponent
        if combatant.is_player:
            targets = alive_npcs
        else:
            targets = alive_players
        if not targets:
            self.active = False
            return None
        target = targets[0]

        # Attack roll and damage
        attack_roll = roll_d20()
        damage = roll_d6()
        critical = attack_roll == 20
        if critical:
            damage *= 2
        target.hp -= damage
        message = (
            f"{combatant.name} attacks {target.name} (roll {attack_roll}) "
            f"for {damage} damage{' (critical)' if critical else ''}."
        )

        # Advance turn index
        self.current_index = (self.current_index + 1) % len(self.round_order)
        return combatant, message
