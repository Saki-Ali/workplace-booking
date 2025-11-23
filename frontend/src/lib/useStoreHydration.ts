import { useEffect, useState } from 'react';
import { useAppStore } from '../store';

// Waits for zustand-persist to rehydrate before rendering protected routes.
export function useStoreHydration() {
  const [hydrated, setHydrated] = useState(useAppStore.persist.hasHydrated());

  useEffect(() => {
    const unsub = useAppStore.persist.onFinishHydration(() => setHydrated(true));
    return () => unsub();
  }, []);

  return hydrated;
}
