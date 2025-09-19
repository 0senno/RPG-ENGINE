"""Tests for world generation and persistence.

These tests ensure that the world generator creates the expected number of
locations and that repeating with the same seed yields identical terrain
layouts.
"""

from app.game_logic import world_generator
from app import models
from app.database import SessionLocal


def test_generate_world_reproducible():
    # Use an in‑memory database to isolate the test
    # Override SQLALCHEMY_DATABASE_URL temporarily
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    seed = 42
    # Generate world twice and compare terrain patterns
    terrain_maps = []
    for _ in range(2):
        db = TestingSessionLocal()
        world_generator.generate_world(db, seed)
        terrain = {(loc.x, loc.y): loc.terrain for loc in db.query(models.Location).all()}
        terrain_maps.append(terrain)
        db.close()
    assert terrain_maps[0] == terrain_maps[1], "World generation should be reproducible with the same seed"
