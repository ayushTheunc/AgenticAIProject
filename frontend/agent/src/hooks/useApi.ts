import { useEffect, useRef, useState } from 'react';
import { ApiError } from '../lib/types';

// Small generic hook to wrap service calls without pulling in extra deps.
// If you prefer TanStack Query, you can swap this out in one place.
export function useApi<T>(
  fn: (...args: any[]) => Promise<T>,
  args: any[] = [],
  options: { immediate?: boolean } = { immediate: true }
) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<ApiError | null>(null);
  const [loading, setLoading] = useState<boolean>(!!options.immediate);
  const abortRef = useRef<AbortController | null>(null);

  async function execute(...callArgs: any[]) {
    setLoading(true);
    setError(null);
    abortRef.current?.abort();
    const ctrl = new AbortController();
    abortRef.current = ctrl;
    try {
      const res = await fn(...(callArgs.length ? callArgs : args), { signal: ctrl.signal });
      setData(res);
      return res;
    } catch (e: any) {
      setError(e);
      throw e;
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (options.immediate) execute();
    return () => abortRef.current?.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { data, error, loading, execute, setData };
}
