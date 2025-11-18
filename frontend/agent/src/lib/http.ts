// Minimal fetch wrapper tuned for FastAPI.
// - Adds base URL + JSON headers
// - Reads auth token from localStorage
// - Throws ApiError on non-2xx with FastAPI-style payloads
import { env } from './env';
import { ApiError, ApiErrorPayload, HttpMethod } from './types';

type RequestOptions = {
  method?: HttpMethod;
  headers?: Record<string, string>;
  body?: unknown;
  // If a route needs no auth (e.g., /auth/login), pass { auth: false }
  auth?: boolean;
  signal?: AbortSignal;
};

function getAuthToken(): string | null {
  try {
    return localStorage.getItem(env.authStorageKey);
  } catch {
    return null;
  }
}

export async function http<T>(path: string, options: RequestOptions = {}): Promise<T> {
  if (!env.apiBaseUrl) {
    throw new Error('API base URL is not configured. Set VITE_API_BASE_URL in your .env.');
  }

  const url = path.startsWith('http') ? path : `${env.apiBaseUrl}${path}`;
  const headers: Record<string, string> = {
    'Accept': 'application/json',
    ...(options.body ? { 'Content-Type': 'application/json' } : {}),
    ...(options.headers || {}),
  };

  // Attach bearer token by default
  const useAuth = options.auth !== false;
  const token = useAuth ? getAuthToken() : null;
  if (useAuth && token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(url, {
    method: options.method || 'GET',
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
    signal: options.signal,
    credentials: 'include', // useful if FastAPI uses cookies
  });

  const text = await res.text();
  const contentType = res.headers.get('content-type') || '';
  const isJson = contentType.includes('application/json');
  const data = isJson && text ? JSON.parse(text) : (text as unknown);

  if (!res.ok) {
    const payload = (isJson ? data : { detail: text || res.statusText }) as ApiErrorPayload;
    const message = typeof payload?.detail === 'string' ? payload.detail : res.statusText;
    throw new ApiError(message || 'Request failed', res.status, payload);
  }

  return data as T;
}

// Convenience helpers
export const get = <T>(path: string, options?: Omit<RequestOptions, 'method'|'body'>) => http<T>(path, { ...options, method: 'GET' });
export const post = <T>(path: string, body?: unknown, options?: Omit<RequestOptions, 'method'|'body'>) => http<T>(path, { ...options, method: 'POST', body });
export const put =  <T>(path: string, body?: unknown, options?: Omit<RequestOptions, 'method'|'body'>) => http<T>(path, { ...options, method: 'PUT', body });
export const patch =<T>(path: string, body?: unknown, options?: Omit<RequestOptions, 'method'|'body'>) => http<T>(path, { ...options, method: 'PATCH', body });
export const del =  <T>(path: string, options?: Omit<RequestOptions, 'method'|'body'>) => http<T>(path, { ...options, method: 'DELETE' });
