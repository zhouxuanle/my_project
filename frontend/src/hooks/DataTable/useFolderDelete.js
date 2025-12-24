import { useState, useCallback, useRef, useEffect } from 'react';

export default function useFolderDelete(onDeleteFolder) {
  const [deletingFolder, setDeletingFolder] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [deleteError, setDeleteError] = useState(null);
  
  // Use ref to track latest confirmDelete without causing re-renders
  const confirmDeleteRef = useRef(null);
  
  useEffect(() => {
    confirmDeleteRef.current = confirmDelete;
  }, [confirmDelete]);

  const handleDeleteClick = useCallback((e, folderOrFolders) => {
    if (e) e.stopPropagation();
    setConfirmDelete(folderOrFolders);
    setDeleteError(null);
  }, []);

  const handleConfirmDelete = useCallback(async () => {
    const currentConfirmDelete = confirmDeleteRef.current;
    if (!currentConfirmDelete) return;
    
    const foldersToDelete = Array.isArray(currentConfirmDelete) ? currentConfirmDelete : [currentConfirmDelete];
    setDeletingFolder(foldersToDelete.length === 1 ? foldersToDelete[0] : 'multiple');
    setDeleteError(null);

    try {
      // Delete all folders in parallel
      await Promise.all(foldersToDelete.map(folder => onDeleteFolder(folder)));
      setConfirmDelete(null);
    } catch (error) {
      console.error('Delete error:', error);
      setDeleteError(error.message || 'Failed to delete folder(s)');
    } finally {
      setDeletingFolder(null);
    }
  }, [onDeleteFolder]); // Removed confirmDelete from deps

  const handleCancelDelete = useCallback(() => {
    setConfirmDelete(null);
    setDeleteError(null);
  }, []);

  return {
    deletingFolder,
    confirmDelete,
    deleteError,
    handleDeleteClick,
    handleConfirmDelete,
    handleCancelDelete,
  };
}
