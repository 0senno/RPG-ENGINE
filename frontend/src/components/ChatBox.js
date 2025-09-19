import React from 'react';

export default function ChatBox({ messages }) {
  return (
    <div className="bg-white p-2 border h-40 overflow-y-auto mb-2">
      <h2 className="font-bold mb-2">Dialogue</h2>
      {messages && messages.slice(-5).map((msg, idx) => (
        <div key={idx} className="text-sm text-gray-800 mb-1">
          {msg}
        </div>
      ))}
      {(!messages || messages.length === 0) && <div className="text-sm text-gray-500">No dialogue yet.</div>}
    </div>
  );
}
