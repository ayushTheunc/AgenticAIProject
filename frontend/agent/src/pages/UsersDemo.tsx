import React, { useState } from 'react';
import { useUsers } from '../hooks/useUsers';

// Demo page to prove the pattern end-to-end.
// Replace with your actual feature pages.
const UsersDemo: React.FC = () => {
  const { list, create } = useUsers();
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">Users (Demo)</h1>

      {list.loading && <p>Loading users…</p>}
      {list.error && <p className="text-red-600">Error: {list.error.message}</p>}

      <form className="flex gap-2" onSubmit={async (e) => {
        e.preventDefault();
        await create({ email, name } as any);
        setEmail(''); setName('');
      }}>
        <input
          className="border rounded p-2 flex-1"
          placeholder="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          className="border rounded p-2 flex-1"
          placeholder="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button className="border rounded px-4 py-2" type="submit">Add</button>
      </form>

      <ul className="space-y-2">
        {(list.data || []).map(u => (
          <li key={u.id} className="border rounded p-3">
            <div className="font-medium">{u.name}</div>
            <div className="text-sm text-neutral-600">{u.email}</div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UsersDemo;
