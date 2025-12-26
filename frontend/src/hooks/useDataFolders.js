import { useCallback, useEffect, useState } from 'react';
import { api } from '../services/api';
import useDataStore from '../stores/HomePage/dataStore';

export default function useDataFolders({ autoFetch = false } = {}) {
  const { 
    folders, 
    error, 
    hasFolder,
    setFolders,
    setError,
  } = useDataStore();

  const [loading, setLoading] = useState(autoFetch);

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

  const deleteFolder = useCallback(async (parentJobId) => {
    try {
      const res = await api.deleteFolder(parentJobId);
      const data = await res.json();
      
      if (data.success) {
        await fetchFolders();
        return { success: true };
      } else {
        throw new Error(data.message || 'Failed to delete folder');
      }
    } catch (err) {
      setError(err);
      throw err;
    }
  }, [fetchFolders]);

  useEffect(() => {
    if (autoFetch) fetchFolders();
  }, [autoFetch, fetchFolders]);

  return {
    folders,
    loading,
    error,
    refresh: fetchFolders,
    deleteFolder,
    hasFolder,
  };
}
