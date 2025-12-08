import { useCallback, useEffect, useState } from 'react';
import { api } from '../services/api';

export default function useDataFolders({ autoFetch = false } = {}) {
  const [folders, setFolders] = useState([]);
  const [loading, setLoading] = useState(autoFetch);
  const [error, setError] = useState(null);

  const fetchFolders = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.listParentJobs();
      const data = await res.json();
      if (data && Array.isArray(data.parentJobIds)) {
        setFolders(data.parentJobIds);
      } else {
        setFolders([]);
      }
    } catch (err) {
      setError(err);
      setFolders([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) fetchFolders();
  }, [autoFetch, fetchFolders]);

  return {
    folders,
    loading,
    error,
    refresh: fetchFolders,
    hasFolder: folders.length > 0,
  };
}
