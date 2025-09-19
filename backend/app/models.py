"""SQLAlchemy models representing players, NPCs, locations, items and events.

These models form the persistent schema for the game. Each table has a
corresponding Pydantic schema defined in ``schemas.py`` for serialisation.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class Location(Base):
    """A tile on the world map.

    Each location is part of a 2D grid and stores its terrain type and whether
    it has been discovered by the player. NPCs reference locations via
    ``location_id``.
    """

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Integer, index=True)
    y = Column(Integer, index=True)
    terrain = Column(String, default="plains")
    discovered = Column(Boolean, default=False)
    # Relationship defined on NPC side


class Player(Base):
    """The player character.

    Stores stats such as hit points and survival conditions along with the
    player's current position on the map. Inventory items are stored in a
    separate table and linked via a relationship.
    """

    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hp = Column(Integer, default=20)
    hunger = Column(Integer, default=0)
    thirst = Column(Integer, default=0)
    fatigue = Column(Integer, default=0)
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)
    # relationship to inventory
    inventory_items = relationship("InventoryItem", back_populates="owner")


class NPC(Base):
    """Non‑player character with personality traits and world position."""

    __tablename__ = "npcs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hp = Column(Integer, default=10)
    # Personality axes range from -1 (hostile/greedy/secretive) to +1
    kindness = Column(Float, default=0.0)
    greed = Column(Float, default=0.0)
    curiosity = Column(Float, default=0.0)
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    location = relationship("Location")


class Item(Base):
    """Master list of all possible items. Items can be stackable or unique."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, default="")
    stackable = Column(Boolean, default=True)


class InventoryItem(Base):
    """A particular item in a player's inventory with a quantity."""

    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("players.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, default=1)

    owner = relationship("Player", back_populates="inventory_items")
    item = relationship("Item")


class Event(Base):
    """Represents a global event such as weather, war or plague."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    timestamp = Column(String)  # ISO 8601 datetime string


def create_all():
    """Initialise the database by creating all tables. Call this during app
    startup or from a CLI script.
    """
    from .database import engine

    Base.metadata.create_all(bind=engine)
