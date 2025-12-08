import { useCallback, useState } from 'react';
import { api } from '../services/api';

export default function useGenerateJob() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const generate = useCallback(async (dataCount) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.generateRawData(dataCount);
      const data = await res.json();
      setResult(data);
      return data;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
    setResult(null);
  }, []);

  return { generate, loading, error, result, reset };
}
