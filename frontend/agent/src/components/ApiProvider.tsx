// Optional: simple toolbar to show current API base + auth status for devs.
import React from 'react';
import { env } from '../lib/env';
import { getToken, logout } from '../services/auth';

export const ApiToolbar: React.FC = () => {
  const token = getToken();
  return (
    <div className="fixed bottom-3 right-3 rounded-xl border px-3 py-2 text-sm opacity-80 bg-white/70 dark:bg-neutral-900/70 backdrop-blur">
      <div><strong>API:</strong> {env.apiBaseUrl || 'NOT SET'}</div>
      <div><strong>Auth:</strong> {token ? 'token present' : 'anonymous'}</div>
      {token && (
        <button className="mt-2 rounded-lg border px-2 py-1 hover:bg-black/5 dark:hover:bg-white/10" onClick={logout}>
          Logout
        </button>
      )}
    </div>
  );
};
