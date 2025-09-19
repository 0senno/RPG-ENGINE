"""FastAPI entry point for the RPG engine backend.

This module wires together the database, world generator, NPC agents, combat
engine and event system into a collection of REST endpoints. It exposes
operations for initialising a world, creating players, moving around the map,
interacting with NPCs and retrieving the world state. The API is stateless
apart from the persisted SQLite database.
"""

from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional

from .database import get_db
from . import models, schemas, crud
from .game_logic import world_generator, combat
from .npc_agent import NPCAgent
from .game_logic.event_system import EventSystem

app = FastAPI(title="AI‑Powered RPG Engine", version="0.1.0")


@app.on_event("startup")
def startup_event():
    """Create database tables on startup."""
    models.create_all()


@app.post("/init", summary="Initialise a new world")
def init_world(seed: Optional[int] = None, db: Session = Depends(get_db)):
    """(Re)generate the world. All existing data will be overwritten.

    Passing a seed allows reproducible world generation. This endpoint also
    resets all events and players. Use with caution.
    """
    # Delete events and players
    db.query(models.Event).delete()
    db.query(models.Player).delete()
    db.commit()
    world_generator.generate_world(db, seed)
    return {"message": "World initialised", "seed": seed}


@app.post("/players", response_model=schemas.Player)
def create_player(request: schemas.CreatePlayerRequest, db: Session = Depends(get_db)):
    """Create a new player with default stats and place them at the origin (0,0)."""
    if crud.get_player_by_name(db, request.name):
        raise HTTPException(status_code=400, detail="Player name already exists")
    player = crud.create_player(db, request.name)
    return player


@app.get("/players/{player_id}", response_model=schemas.Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).get(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@app.post("/players/{player_id}/move")
def move_player(player_id: int, move: schemas.MoveRequest, db: Session = Depends(get_db)):
    """Move a player by dx/dy. Discover the new location and trigger NPC ticks and events."""
    player = db.query(models.Player).get(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    # Update position within bounds
    new_x = max(0, min(world_generator.WORLD_SIZE - 1, player.x + move.dx))
    new_y = max(0, min(world_generator.WORLD_SIZE - 1, player.y + move.dy))
    player.x, player.y = new_x, new_y
    db.commit()
    # Discover location
    crud.set_location_discovered(db, new_x, new_y)
    # Tick NPCs at the new location
    npcs = crud.get_npcs_at(db, new_x, new_y)
    messages: List[str] = []
    for npc in npcs:
        agent = NPCAgent(npc, db)
        msg = agent.tick()
        if msg:
            messages.append(msg)
            crud.create_event(db, msg)
    # Trigger random event
    event_system = EventSystem(db)
    random_event = event_system.maybe_trigger()
    if random_event:
        messages.append(random_event.description)
    return {"x": new_x, "y": new_y, "messages": messages}


@app.post("/players/{player_id}/talk")
def talk_to_npc(
    player_id: int,
    request: schemas.TalkRequest = Body(...),
    db: Session = Depends(get_db),
):
    """Initiate dialogue with an NPC at the player's current location."""
    player = db.query(models.Player).get(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    npc = db.query(models.NPC).get(request.npc_id)
    if not npc or npc.x != player.x or npc.y != player.y:
        raise HTTPException(status_code=400, detail="NPC not at player's location")
    agent = NPCAgent(npc, db)
    message = agent.act("talk")
    crud.create_event(db, message)
    return {"message": message}


@app.post("/players/{player_id}/attack")
def attack_npc(player_id: int, request: schemas.AttackRequest, db: Session = Depends(get_db)):
    """Start a combat encounter between the player and the target NPC."""
    player = db.query(models.Player).get(player_id)
    npc = db.query(models.NPC).get(request.target_id)
    if not player or not npc:
        raise HTTPException(status_code=404, detail="Invalid combatants")
    combatants = [
        combat.Combatant(name=player.name, hp=player.hp, is_player=True, entity=player),
        combat.Combatant(name=npc.name, hp=npc.hp, is_player=False, entity=npc),
    ]
    encounter = combat.CombatEncounter(combatants)
    log: List[str] = []
    while encounter.active:
        result = encounter.next_turn()
        if result:
            _combatant, msg = result
            log.append(msg)
    # Update HP back into the models
    player.hp = combatants[0].hp
    npc.hp = combatants[1].hp
    db.commit()
    # Persist combat log as events
    for line in log:
        crud.create_event(db, line)
    return {"log": log}


@app.get("/world")
def get_visible_world(player_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Return all discovered locations, or if player_id provided only those discovered by the player.

    In this demo implementation discovery is global; a location is either
    discovered or not regardless of who found it. Future work could track
    discovery per player.
    """
    locations = db.query(models.Location).filter(models.Location.discovered == True).all()
    return {"locations": [schemas.Location.from_orm(loc) for loc in locations]}


@app.get("/events", response_model=List[schemas.Event])
def list_events(db: Session = Depends(get_db)):
    events = db.query(models.Event).order_by(models.Event.id.desc()).all()
    return events
