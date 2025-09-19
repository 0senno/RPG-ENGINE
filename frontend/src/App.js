import React, { useEffect, useState } from 'react';
import Map from './components/Map';
import EventLog from './components/EventLog';
import ChatBox from './components/ChatBox';
import Inventory from './components/Inventory';

function App() {
  const [player, setPlayer] = useState(null);
  const [world, setWorld] = useState([]);
  const [events, setEvents] = useState([]);
  const [messages, setMessages] = useState([]);

  // Initialise player and world on mount
  useEffect(() => {
    async function init() {
      // Check if player exists. Create one named "Hero" if not.
      let playerData = null;
      try {
        const res = await fetch('/api/players');
        // Not implemented: index endpoint. We'll attempt to create a player instead.
      } catch (err) {
        // ignore
      }
      const createRes = await fetch('/api/players', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'Hero' }),
      });
      if (createRes.ok) {
        playerData = await createRes.json();
      }
      setPlayer(playerData);
      // Fetch world
      await fetchWorld();
      // Fetch events
      await fetchEvents();
    }
    init();
  }, []);

  async function fetchWorld() {
    const res = await fetch('/api/world');
    if (res.ok) {
      const data = await res.json();
      setWorld(data.locations);
    }
  }

  async function fetchEvents() {
    const res = await fetch('/api/events');
    if (res.ok) {
      const data = await res.json();
      setEvents(data);
    }
  }

  async function move(dx, dy) {
    if (!player) return;
    const res = await fetch(`/api/players/${player.id}/move`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dx, dy }),
    });
    if (res.ok) {
      const data = await res.json();
      // Update player position
      setPlayer({ ...player, x: data.x, y: data.y });
      // Append messages
      setMessages((msgs) => [...msgs, ...data.messages]);
      // Refresh world and events
      await fetchWorld();
      await fetchEvents();
    }
  }

  if (!player) {
    return (
      <div className="p-4">Loading player...</div>
    );
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">AI‑Powered RPG</h1>
      <div className="grid grid-cols-3 gap-4">
        <div>
          <Map world={world} player={player} onMove={move} />
        </div>
        <div>
          <EventLog events={events} messages={messages} />
        </div>
        <div>
          <ChatBox messages={messages} />
          <Inventory inventory={player.inventory_items} />
        </div>
      </div>
    </div>
  );
}

export default App;
