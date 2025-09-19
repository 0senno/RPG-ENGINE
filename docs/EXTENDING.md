# Extending the AI‑Powered RPG Engine

This guide explains how to add your own content and mechanics to the engine. All
data files live under the `data/` directory and game logic is modularised in
Python packages under `backend/app/`.

## Adding new items

Items are defined in the `items` table in the database and can be created at
runtime via the API or seeded during world generation. To add predefined
starting items for a new campaign:

1. Open `data/example_world.json` and add entries to the `items` list. Each
   item must have a unique name and may include a description.
2. When writing your own generator (see below) insert these items into the
   database using the SQLAlchemy models in `backend/app/models.py`.
3. Update any NPCs or quests that reference the new items.

## Adding NPC archetypes

NPCs are spawned during world generation in
`backend/app/game_logic/world_generator.py`. Each archetype defines the NPC’s
`name` and personality axes `kindness`, `greed` and `curiosity`. To add a new
archetype, append a dictionary to the `NPC_ARCHETYPES` list with appropriate
values. For example:

```python
NPC_ARCHETYPES.append({
    "name": "Zara the Witch",
    "kindness": -0.8,
    "greed": 0.5,
    "curiosity": 0.9,
})
```

The world generator will automatically place the new NPC at a random location
whenever a new world is created.

## Writing your own quests

Quests are not currently persisted in the database but you can model them in a
similar fashion to NPCs. Define a `Quest` SQLAlchemy model with fields such as
`title`, `description`, `giver_npc_id` and `target_location`. Then create
Pydantic schemas for API responses and add endpoints for listing and updating
quests.

## Custom genres and rules

The engine ships with fantasy‑style mechanics by default but you can add new
genres such as sci‑fi or post‑apocalyptic survival. To do so:

1. Create a new module under `backend/app/game_logic/` (e.g. `sci_fi.py`) and
   implement genre‑specific systems such as space travel or radiation effects.
2. Define new terrain types in `TERRAINS` within `world_generator.py` or
   override `generate_world` to build a hex map or planet grid.
3. Extend the `NPCAgent` to include behaviours unique to your setting (e.g.
   hacking, piloting).

## Save and load profiles

Saving and loading is handled by copying the SQLite database file to and from
the `data/saves/` directory. The default endpoints in `main.py` do not expose
this feature yet; however, you can implement a `/save/{profile_name}` endpoint
that calls `shutil.copy('game.db', f'data/saves/{profile_name}.db')` and a
`/load/{profile_name}` endpoint that restores it. Be sure to close all database
connections before copying the file.

## Exporting adventure logs

To export a session as Markdown or PDF you can fetch all events from `/events`
and format them into a narrative. The Python `markdown` and `weasyprint`
libraries can help with conversion. You could add an endpoint that returns
rendered HTML and call an external PDF service to generate the final file.

## Contributing

Feel free to submit pull requests with new systems, bug fixes or documentation
improvements. This project is an early prototype and many features remain to
be implemented. Contributions that expand the engine without breaking
existing functionality are especially welcome.
