import React from 'react';

export default function Inventory({ inventory }) {
  return (
    <div className="bg-white p-2 border h-40 overflow-y-auto">
      <h2 className="font-bold mb-2">Inventory</h2>
      {inventory && inventory.length > 0 ? (
        <ul className="text-sm">
          {inventory.map((inv) => (
            <li key={inv.id}>
              {inv.item.name} x{inv.quantity}
            </li>
          ))}
        </ul>
      ) : (
        <div className="text-sm text-gray-500">Your bag is empty.</div>
      )}
    </div>
  );
}
