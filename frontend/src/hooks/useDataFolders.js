import { useCallback, useEffect, useState } from 'react';
import { api } from '../services/api';
import useDataStore from '../stores/HomePage/dataStore';

export default function useDataFolders({ autoFetch = false } = {}) {
  const [folders, setFolders] = useState([]);
  const [loading, setLoading] = useState(autoFetch);
  const [error, setError] = useState(null);

  const { hasFolder, setHasFolder } = useDataStore();

  const fetchFolders = useCallback(async () => {
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
  }, []); // Empty deps - setHasFolder is stable from Zustand store

  const deleteFolder = useCallback(async (parentJobId) => {
    try {
      const res = await api.deleteFolder(parentJobId);
      const data = await res.json();
      
      if (data.success) {
        // Refresh the folder list from server to ensure consistency
        await fetchFolders();
        return { success: true };
      } else {
        throw new Error(data.message || 'Failed to delete folder');
      }
    } catch (err) {
      // If 404, folder is already gone - refresh list and treat as success
      if (err.status === 404) {
        await fetchFolders();
        return { success: true };
      }
      setError(err);
      throw err;
    }
  }, [fetchFolders]); // Removed setError - it's a stable setState function

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
