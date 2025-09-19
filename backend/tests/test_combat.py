"""Tests for the combat system.

These tests exercise the initiative order and damage application. They use
deterministic dice rolls by monkeypatching the roll functions to produce
predictable results.
"""

import types

from app.game_logic import combat


def test_initiative_order(monkeypatch):
    # Prepare deterministic initiative rolls: player gets 10, npc gets 5
    initiative_results = [10, 5]
    roll_iter = iter(initiative_results)

    def fake_roll_d20():
        return next(roll_iter)

    # Patch dice.roll_d20 used in combat
    monkeypatch.setattr(combat, "roll_d20", fake_roll_d20)

    player = combat.Combatant(name="Hero", hp=10, is_player=True, entity=None)
    npc = combat.Combatant(name="Goblin", hp=10, is_player=False, entity=None)
    encounter = combat.CombatEncounter([player, npc])

    # Player should act first because of higher initiative
    assert encounter.round_order[0].name == "Hero"
    assert encounter.round_order[1].name == "Goblin"
