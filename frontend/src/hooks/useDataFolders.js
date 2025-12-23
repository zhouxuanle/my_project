import { useCallback, useEffect, useState } from 'react';
import { api } from '../services/api';
import useDataStore from '../stores/HomePage/dataStore';

export default function useDataFolders({ autoFetch = false } = {}) {
  const [folders, setFolders] = useState([]);
  const [loading, setLoading] = useState(autoFetch);
  const [error, setError] = useState(null);

  const { hasFolder, setHasFolder } = useDataStore();

  const fetchFolders = useCallback(async () => {
    console.log('Fetching data folders...');
    setLoading(true);
    setError(null);
    try {
      const res = await api.listParentJobs();
      const data = await res.json();
      if (data && Array.isArray(data.parentJobIds)) {
        setFolders(data.parentJobIds);
        setHasFolder(data.parentJobIds.length > 0);
      } else {
        setFolders([]);
        setHasFolder(false);
      }
    } catch (err) {
      setError(err);
      setFolders([]);
      setHasFolder(false);
    } finally {
      setLoading(false);
    }
    console.log('hasFolder:', hasFolder)
  }, [setHasFolder]);

  useEffect(() => {
    if (autoFetch) fetchFolders();
  }, [autoFetch, fetchFolders]);

  return {
    folders,
    loading,
    error,
    refresh: fetchFolders,
    hasFolder,
  };
}
