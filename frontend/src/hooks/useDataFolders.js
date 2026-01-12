import { useCallback, useEffect, useState } from 'react';
import { api } from '../services/api';
import useDataStore from '../stores/HomePage/dataStore';
import useLayoutStore from '../stores/Layout/layoutStore';

export default function useDataFolders({ autoFetch = false } = {}) {
  const { 
    folders, 
    error, 
    hasFolder,
    setFolders,
    setError,
  } = useDataStore();
  const { addNotification } = useLayoutStore();

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
        // Create success notification data
        const deletedFolders = Array.isArray(parentJobId) ? parentJobId : [parentJobId];
        const folderNames = deletedFolders.join(', ');
        const notificationMsg = `Successfully deleted ${deletedFolders.length === 1 ? 'folder' : 'folders'}: ${folderNames}`;
        
        // Save notification to backend
        const saveRes = await api.saveNotification(notificationMsg, 'completed');
        const saveData = await saveRes.json();
        
        if (saveData.notification_id) {
          addNotification('job', {
            id: saveData.notification_id,
            message: notificationMsg,
            status: 'completed',
            timestamp: new Date().toISOString()
          });
        }
        
        return { success: true };
      } else {
        throw new Error(data.message || 'Failed to delete folder');
      }
    } catch (err) {
      setError(err);
      
      // Refetch folders to ensure UI matches backend state after failure
      await fetchFolders();
      
      // Create and save error notification
      const deletedFolders = Array.isArray(parentJobId) ? parentJobId : [parentJobId];
      const folderNames = deletedFolders.join(', ');
      const errorMsg = `Failed to delete ${deletedFolders.length === 1 ? 'folder' : 'folders'}: ${folderNames}. ${err.message}`;
      
      const saveRes = await api.saveNotification(errorMsg, 'failed');
      const saveData = await saveRes.json();
      
      if (saveData.notification_id) {
        addNotification('job', {
          id: saveData.notification_id,
          message: errorMsg,
          status: 'failed',
          timestamp: new Date().toISOString()
        });
      }
      
      throw err;
    }
  }, [folders, setFolders, addNotification]);

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
