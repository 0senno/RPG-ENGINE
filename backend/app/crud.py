"""CRUD helpers for interacting with the database.

These functions encapsulate common operations on models such as retrieving a
player by name, creating a new NPC or updating location discovery. They take a
SQLAlchemy session as the first argument and return SQLAlchemy objects.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from . import models


def get_player_by_name(db: Session, name: str) -> Optional[models.Player]:
    return db.query(models.Player).filter(models.Player.name == name).first()


def create_player(db: Session, name: str) -> models.Player:
    player = models.Player(name=name)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def get_locations(db: Session) -> List[models.Location]:
    return db.query(models.Location).all()


def set_location_discovered(db: Session, x: int, y: int) -> None:
    loc = (
        db.query(models.Location)
        .filter(models.Location.x == x, models.Location.y == y)
        .first()
    )
    if loc:
        loc.discovered = True
        db.commit()


def get_npcs_at(db: Session, x: int, y: int) -> List[models.NPC]:
    return db.query(models.NPC).filter(models.NPC.x == x, models.NPC.y == y).all()


def create_event(db: Session, description: str) -> models.Event:
    event = models.Event(description=description, timestamp=datetime.utcnow().isoformat())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
