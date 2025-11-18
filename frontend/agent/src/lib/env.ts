// Centralized env access so we don't scatter process.env/VITE_* everywhere.
export const env = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL as string,
  authStorageKey: (import.meta.env.VITE_AUTH_STORAGE_KEY as string) || 'authToken',
};

if (!env.apiBaseUrl) {
  // This helps new devs immediately see what's missing.
  // The app will still compile but network calls will throw a helpful error.
  console.warn('[env] VITE_API_BASE_URL is not set. API calls will fail until it is configured.');
}
