import React from 'react';

// Determine world size by finding max coordinates
function getWorldSize(world) {
  let maxX = 0;
  let maxY = 0;
  for (const loc of world) {
    if (loc.x > maxX) maxX = loc.x;
    if (loc.y > maxY) maxY = loc.y;
  }
  return { width: maxX + 1, height: maxY + 1 };
}

export default function Map({ world, player, onMove }) {
  const { width, height } = getWorldSize(world);
  // Create a set of discovered coordinates for quick lookup
  const discovered = new Set(world.map((loc) => `${loc.x},${loc.y}`));

  const rows = [];
  for (let y = 0; y < height; y++) {
    const cells = [];
    for (let x = 0; x < width; x++) {
      const key = `${x},${y}`;
      const isPlayer = player.x === x && player.y === y;
      const isDiscovered = discovered.has(key);
      cells.push(
        <div
          key={key}
          className={`w-4 h-4 border ${isDiscovered ? 'bg-green-200' : 'bg-gray-400'} ${isPlayer ? 'border-2 border-red-500' : ''}`}
        />
      );
    }
    rows.push(
      <div key={y} className="flex">
        {cells}
      </div>
    );
  }

  return (
    <div>
      <div className="mb-2">
        <div className="flex justify-center mb-1">
          <button onClick={() => onMove(0, -1)} className="px-2 py-1 bg-blue-500 text-white rounded">↑</button>
        </div>
        <div className="flex justify-between">
          <button onClick={() => onMove(-1, 0)} className="px-2 py-1 bg-blue-500 text-white rounded">←</button>
          <button onClick={() => onMove(1, 0)} className="px-2 py-1 bg-blue-500 text-white rounded">→</button>
        </div>
        <div className="flex justify-center mt-1">
          <button onClick={() => onMove(0, 1)} className="px-2 py-1 bg-blue-500 text-white rounded">↓</button>
        </div>
      </div>
      <div className="border border-gray-500 inline-block">
        {rows}
      </div>
    </div>
  );
}
