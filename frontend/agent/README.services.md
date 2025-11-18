# Frontend Services Scaffold (Vite + React + TS)

## What this gives you
- A tiny HTTP client pre-wired for FastAPI (JWT or cookie auth)
- Centralized env config (VITE_API_BASE_URL, VITE_AUTH_STORAGE_KEY)
- Service layer pattern (`src/services/*`) with typed endpoints
- Lightweight `useApi` hook (can be swapped to TanStack Query later)
- Demo page showing how to fetch/create users
- Dev toolbar to see current API base + auth status
- FastAPI CORS snippet to drop into your backend

## Quick start
1) Copy the `src/` folder pieces you want into your Vite project.
2) Create `.env` from `.env.example` and set `VITE_API_BASE_URL` (e.g., http://localhost:8000).
3) Wire `<App />` or route `/pages/UsersDemo` into your app to test.
4) On the backend, add the provided CORS middleware config.

## Conventions
- Put feature endpoints in `src/services/<feature>.ts`
- Add tiny hooks in `src/hooks` that wire services to components
- Keep comments brief but contextual so other devs understand intent quickly
