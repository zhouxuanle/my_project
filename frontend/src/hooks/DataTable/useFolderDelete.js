import { useState, useCallback } from 'react';
import useDataTableStore from '../../stores/DataTable/dataTableStore';

export default function useFolderDelete(onDeleteFolder, folders = []) {
  const { selectedFolders, setSelectedFolders } = useDataTableStore();
  const [deletingFolder, setDeletingFolder] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [deleteError, setDeleteError] = useState(null);

  const handleToggleFolder = useCallback((folder) => {
    setSelectedFolders(
      selectedFolders.includes(folder)
        ? selectedFolders.filter(f => f !== folder)
        : [...selectedFolders, folder]
    );
  }, [selectedFolders]);

  const handleSelectAll = useCallback(() => {
    setSelectedFolders(
      selectedFolders.length === folders.length ? [] : [...folders]
    );
  }, [folders, selectedFolders]);

  const handleDeleteClick = useCallback((folderOrFolders) => {
    setConfirmDelete(folderOrFolders);
    setDeleteError(null);
  }, []);

  const handleConfirmDelete = useCallback(async () => {
    const foldersToDelete = Array.isArray(confirmDelete) ? confirmDelete : [confirmDelete];
    setDeletingFolder(foldersToDelete.length === 1 ? foldersToDelete[0] : 'multiple');
    setDeleteError(null);

    try {
      // Delete all folders in parallel
      await Promise.all(foldersToDelete.map(folder => onDeleteFolder(folder)));
      setConfirmDelete(null);
      setSelectedFolders([]);
    } catch (error) {
      console.error('Delete error:', error);
      setDeleteError(error.message || 'Failed to delete folder(s)');
    } finally {
      setDeletingFolder(null);
    }
  }, [onDeleteFolder, confirmDelete]);

  const handleCancelDelete = useCallback(() => {
    setConfirmDelete(null);
    setDeleteError(null);
  }, []);

  return {
    selectedFolders,
    deletingFolder,
    confirmDelete,
    deleteError,
    handleToggleFolder,
    handleSelectAll,
    handleDeleteClick,
    handleConfirmDelete,
    handleCancelDelete,
  };
}
