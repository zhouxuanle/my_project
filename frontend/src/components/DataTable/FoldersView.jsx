import React, { useState, useCallback } from 'react';
import Button from '../ui/Button';
import FolderCard from './FolderCard';
import DeleteConfirmationModal from './DeleteConfirmationModal';
import useFolderDelete from '../../hooks/DataTable/useFolderDelete';

function FoldersView({
  foldersLoading,
  foldersError,
  folders,
  onSelectFolder,
  onBackToTables,
  onDeleteFolder,
}) {
  const [isDeleteMode, setIsDeleteMode] = useState(false);
  const [selectedFolders, setSelectedFolders] = useState([]);

  const {
    deletingFolder,
    confirmDelete,
    deleteError,
    handleDeleteClick,
    handleConfirmDelete,
    handleCancelDelete,
  } = useFolderDelete(onDeleteFolder);

  const handleToggleDeleteMode = useCallback(() => {
    setIsDeleteMode(prev => !prev);
    setSelectedFolders([]);
  }, []);

  const handleToggleFolder = useCallback((folder) => {
    setSelectedFolders(prev => 
      prev.includes(folder) 
        ? prev.filter(f => f !== folder)
        : [...prev, folder]
    );
  }, []);

  const handleConfirmSelection = useCallback(() => {
    if (selectedFolders.length > 0) {
      handleDeleteClick(null, selectedFolders);
    }
  }, [selectedFolders, handleDeleteClick]);

  const handleBulkDeleteConfirm = useCallback(async () => {
    await handleConfirmDelete();
    setIsDeleteMode(false);
    setSelectedFolders([]);
  }, [handleConfirmDelete]);

  const handleBulkDeleteCancel = useCallback(() => {
    handleCancelDelete();
  }, [handleCancelDelete]);

  return (
    <div className="flex flex-col items-center w-full px-4">
      <h2 className="text-3xl font-bold mb-8">Your Data Folders</h2>
      
      <div className="w-full max-w-2xl">
        {foldersLoading && (
          <div className="text-center text-gray-400 py-8">Loading folders...</div>
        )}
        
        {foldersError && (
          <div className="text-red-400 text-center py-4">
            {foldersError.message || 'Failed to fetch folders'}
          </div>
        )}
        
        {!foldersLoading && !foldersError && folders.length === 0 && (
          <div className="text-gray-400 text-center py-8">No folders found.</div>
        )}

        {!foldersLoading && !foldersError && folders.length > 0 && (
          <>
            <div className="mb-4 flex gap-3">
              <Button
                variant={isDeleteMode ? "secondary" : "primary"}
                onClick={handleToggleDeleteMode}
              >
                {isDeleteMode ? 'Cancel' : 'Delete Folders'}
              </Button>
              {isDeleteMode && selectedFolders.length > 0 && (
                <Button
                  variant="primary"
                  onClick={handleConfirmSelection}
                >
                  Confirm ({selectedFolders.length})
                </Button>
              )}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
              {folders.map((folder) => (
                <FolderCard
                  key={folder}
                  folder={folder}
                  onSelect={onSelectFolder}
                  isDeleteMode={isDeleteMode}
                  isSelected={selectedFolders.includes(folder)}
                  onToggleSelect={handleToggleFolder}
                  isDeleting={deletingFolder === folder}
                />
              ))}
            </div>
          </>
        )}

        <div className="flex justify-center mt-8">
          <Button variant="secondary" onClick={onBackToTables}>
            Back to tables
          </Button>
        </div>
      </div>

      {confirmDelete && (
        <DeleteConfirmationModal
          folderName={confirmDelete}
          error={deleteError}
          onConfirm={handleBulkDeleteConfirm}
          onCancel={handleBulkDeleteCancel}
        />
      )}
    </div>
  );
}

export default FoldersView;
