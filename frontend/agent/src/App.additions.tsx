import React from 'react';
import UsersDemo from './pages/UsersDemo';
import { ApiToolbar } from './components/ApiProvider';

// Minimal App — you can replace with your router.
export default function App() {
  return (
    <div className="min-h-screen">
      <UsersDemo />
      <ApiToolbar />
    </div>
  );
}
