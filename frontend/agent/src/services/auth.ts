// Auth service: login/logout + token storage conventions.
import { post } from '../lib/http';
import { env } from '../lib/env';

export interface LoginInput { username: string; password: string; }
export interface LoginResponse { access_token: string; token_type: string; }

export async function login(input: LoginInput): Promise<void> {
  // Typical FastAPI JWT endpoint: POST /auth/login with form or JSON
  const res = await post<LoginResponse>('/auth/login', input, { auth: false });
  localStorage.setItem(env.authStorageKey, res.access_token);
}

export function logout() {
  localStorage.removeItem(env.authStorageKey);
}

export function getToken(): string | null {
  try { return localStorage.getItem(env.authStorageKey); } catch { return null; }
}
