"""Random event system.

The event system triggers pseudo‑random global events such as weather changes,
ambushes or diplomatic developments. Events are persisted via the Event model
and broadcast to connected clients through the API. This implementation is
intentionally simple — a real system might schedule events based on a game
clock or player actions.
"""

import random
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from .. import models, crud


class EventSystem:
    def __init__(self, db: Session):
        self.db = db
        self.weather_states = [
            "clear skies",
            "drizzle",
            "thunderstorm",
            "fog",
            "snow",
        ]

    def maybe_trigger(self) -> Optional[models.Event]:
        """Randomly decide whether to trigger an event. Returns the Event if one
        occurred, else None. The probability of an event each call is low to
        avoid spamming the log.
        """
        # 10% chance to trigger a weather event
        if random.random() < 0.1:
            weather = random.choice(self.weather_states)
            description = f"The weather shifts to {weather}."
            return crud.create_event(self.db, description)
        return None
