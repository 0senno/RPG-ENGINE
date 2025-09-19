"""Pydantic schemas used for request/response models.

Schemas provide a contract between the API and its consumers. They are kept
separate from the SQLAlchemy models to avoid accidentally exposing internal
fields such as database IDs.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class LocationBase(BaseModel):
    x: int
    y: int
    terrain: str
    discovered: bool = False


class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    stackable: bool = True

    class Config:
        orm_mode = True


class InventoryItem(BaseModel):
    id: int
    item: Item
    quantity: int

    class Config:
        orm_mode = True


class Player(BaseModel):
    id: int
    name: str
    hp: int
    hunger: int
    thirst: int
    fatigue: int
    x: int
    y: int
    inventory_items: List[InventoryItem] = []

    class Config:
        orm_mode = True


class NPCTraits(BaseModel):
    kindness: float = Field(..., ge=-1.0, le=1.0)
    greed: float = Field(..., ge=-1.0, le=1.0)
    curiosity: float = Field(..., ge=-1.0, le=1.0)


class NPC(BaseModel):
    id: int
    name: str
    hp: int
    x: int
    y: int
    traits: NPCTraits

    class Config:
        orm_mode = True


class Event(BaseModel):
    id: int
    description: str
    timestamp: str

    class Config:
        orm_mode = True


class MoveRequest(BaseModel):
    dx: int
    dy: int


class TalkRequest(BaseModel):
    npc_id: int
    message: Optional[str] = None


class AttackRequest(BaseModel):
    target_id: int


class CreatePlayerRequest(BaseModel):
    name: str
