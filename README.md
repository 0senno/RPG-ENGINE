# AI‑Powered RPG Engine

Welcome to the **AI‑Powered RPG Engine**, a full‑stack role playing framework designed to procedurally generate immersive campaigns, run lightweight NPC agents and persist an evolving world state. This repository contains everything needed to spin up a small scale role‑playing game — including a FastAPI backend with SQLite persistence, a React/TailwindCSS frontend, example data and a handful of demo NPC personalities. The project is heavily modular so you can extend it with your own quests, items, events or even entire genres.

## Features

### Procedural campaigns

The backend can generate a campaign world from a random seed. It creates a 2D map of varied terrain (forests, mountains, rivers and ruins), spawns NPCs with distinct personalities and rolls up a handful of quests to set the story in motion. Dice rolls use fair polyhedral dice — a fair 20‑sided die assigns equal probability to each face due to the uniform symmetry of an icosahedron【171953677326081†L563-L566】. Players take turns moving across the map, talking, crafting or fighting based on a D20‑style action system where each turn allows movement, a free interaction and one action【783174714989504†L23-L40】.

### NPC agents

Each non‑player character is powered by a simple agent loop: **observe → decide → act**. Agents have a personality matrix (e.g. kindness/hostility, greed/generosity, curiosity/secrecy) which influences their decisions. An NPC can speak, trade, fight, betray, ally or wander. Dialogue is procedurally generated from templates and grounded in the NPC’s knowledge and the current world state. Although the built‑in text generator is primitive, the architecture allows you to swap in a proper LLM or connect to a chat API.

### Survival and crafting

Beyond combat and exploration the engine tracks **hunger, thirst and fatigue**. Characters accumulate these conditions over time and they worsen at dawn, noon and dusk; if left unchecked they cause exhaustion【60688443271353†L81-L117】【60688443271353†L148-L161】. Players must eat, drink and rest to recover, adding a survival element to long journeys. A small crafting system lets you combine materials to create tools, weapons and consumables. The rule set draws inspiration from D&D 5e — each turn allows one bonus action, one reaction per round and a single action【783174714989504†L23-L67】.

### Turn‑based combat

Combat uses an initiative system: each participant rolls a d20; the highest result acts first and order remains fixed for the encounter. Attacks, spells and abilities consume the attacker’s action and damage is calculated by rolling appropriate dice. On a natural 20 the attacker scores a critical hit, doubling the rolled damage. Armour reduces incoming damage and the engine supports advantage/disadvantage mechanics. A modest test suite demonstrates fairness and reproducibility.

### Persisted world state

State is saved to a SQLite database via SQLAlchemy. Models track players, NPCs, locations, inventory items, quests and global events. You can save and load multiple profiles, and export an adventure log as Markdown. A random seed system allows reproducible campaigns — feed the same seed into the generator and you’ll get the same world.

### Web UI

The `frontend` directory contains a simple React application styled with TailwindCSS. It presents an interactive map with fog‑of‑war, a chat log for NPC dialogue, a draggable inventory grid and a real‑time event feed. The UI is minimal by design, leaving plenty of room for you to polish or completely replace it. Mockup screenshots live in `docs/assets` to give you a taste of what the interface could look like.

### Extensibility and modding

All content — items, NPC archetypes, quest templates and map tiles — is defined in JSON files under `data/`. To add your own content simply drop a new file in this directory and register it in `docs/EXTENDING.md`. Modders can craft new survival rules, character classes or even genres (fantasy, post‑apocalyptic or sci‑fi) by following the patterns in the existing code.

## Getting started

### Prerequisites

* [Docker](https://www.docker.com/) and Docker Compose
* Node.js ≥ 16 (optional if you intend to build the frontend locally)
* Python ≥ 3.10

### Quick start with Docker

Spin up the backend and frontend using Docker Compose:

```bash
git clone https://github.com/yourusername/rpg_engine.git
cd rpg_engine
docker compose up --build
```

The backend will start on `http://localhost:8000` and the frontend on `http://localhost:5173` by default. Visit the frontend to explore the world, talk to NPCs and watch events unfold.

### Manual setup (development)

1. **Backend**: Create a virtual environment and install dependencies:

   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend**: Install dependencies and run the development server:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   The app uses [Vite](https://vitejs.dev/) for hot module reloading.

### Running tests

Inside `backend` run:

```bash
pytest -q
```

The tests cover dice probability, combat mechanics and world persistence.

## Repository layout

```
rpg_engine/
├── backend/               # FastAPI backend and game logic
│   ├── app/
│   │   ├── main.py        # FastAPI entrypoint and routers
│   │   ├── models.py      # SQLAlchemy models for players, NPCs, items, events
│   │   ├── database.py    # Database session and engine
│   │   ├── schemas.py     # Pydantic schemas for API responses
│   │   ├── crud.py        # CRUD helpers for interacting with the DB
│   │   ├── npc_agent.py   # Mini agent loop for NPC decision making
│   │   └── game_logic/    # Combat engine, dice, events, world generation
│   ├── tests/             # Unit and integration tests
│   ├── requirements.txt   # Backend dependencies
│   └── Dockerfile         # Backend container
├── frontend/
│   ├── src/               # React source code
│   │   ├── components/    # Map, ChatBox, Inventory, EventLog
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── tailwind.config.js # TailwindCSS config
│   ├── package.json       # Frontend dependencies
│   └── Dockerfile         # Frontend container
├── data/                  # Example campaign world, items, quest templates
│   └── example_world.json
├── docs/
│   ├── EXTENDING.md       # Guide for adding custom content
│   └── assets/            # Mockup images of the UI
├── docker-compose.yml     # Compose definition for backend and frontend
├── .github/workflows/ci.yml # GitHub Actions pipeline for linting and tests
└── README.md              # Project overview and instructions
```

## Contributing

Pull requests are welcome! If you plan to make large architectural changes please open an issue first to discuss your ideas. See `docs/EXTENDING.md` for guidance on adding new content.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
