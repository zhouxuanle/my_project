import { useState, useCallback } from 'react';

export default function useSessionStorage(key, initialValue) {
  const readValue = () => {
    try {
      const raw = sessionStorage.getItem(key);
      if (raw !== null) return JSON.parse(raw);
      return initialValue;
    } catch (e) {
      return initialValue;
    }
  };

  const [storedValue, setStoredValue] = useState(readValue());

  const setValue = useCallback((value) => {
    try {
      setStoredValue(value);
      sessionStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      console.warn(`useSessionStorage: failed to set ${key}`, e);
    }
  }, [key]);

  const remove = useCallback(() => {
    try {
      sessionStorage.removeItem(key);
    } catch (e) {
      console.warn(`useSessionStorage: failed to remove ${key}`, e);
    }
    setStoredValue(initialValue);
  }, [key, initialValue]);

  return [storedValue, setValue, remove];
}
