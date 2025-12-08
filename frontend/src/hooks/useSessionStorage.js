import { useState } from 'react';

export default function useSessionStorage(key, initialValue) {
  const readValue = () => {
    try {
      const raw = sessionStorage.getItem(key);
      if (raw !== null) return JSON.parse(raw);
      return typeof initialValue === 'function' ? initialValue() : initialValue;
    } catch (e) {
      // Fall back to initial value on any error
      return typeof initialValue === 'function' ? initialValue() : initialValue;
    }
  };

  const [storedValue, setStoredValue] = useState(readValue);

  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      sessionStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (e) {
      // Non-fatal — log for debugging
      // eslint-disable-next-line no-console
      console.warn(`useSessionStorage: failed to set ${key}`, e);
    }
  };

  const remove = () => {
    try {
      sessionStorage.removeItem(key);
    } catch (e) {
      // eslint-disable-next-line no-console
      console.warn(`useSessionStorage: failed to remove ${key}`, e);
    }
    setStoredValue(typeof initialValue === 'function' ? initialValue() : initialValue);
  };

  return [storedValue, setValue, remove];
}
