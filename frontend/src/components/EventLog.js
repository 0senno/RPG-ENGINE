import React from 'react';

export default function EventLog({ events, messages }) {
  return (
    <div className="bg-white p-2 border h-64 overflow-y-auto">
      <h2 className="font-bold mb-2">Event Log</h2>
      {messages && messages.map((msg, idx) => (
        <div key={`msg-${idx}`} className="text-sm text-gray-700">{msg}</div>
      ))}
      {events && events.map((event) => (
        <div key={event.id} className="text-sm text-gray-500">{event.timestamp}: {event.description}</div>
      ))}
    </div>
  );
}
