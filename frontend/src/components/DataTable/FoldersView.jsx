import React from 'react';
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
  const {
    selectedFolders,
    deletingFolder,
    confirmDelete,
    deleteError,
    handleToggleFolder,
    handleSelectAll,
    handleDeleteClick,
    handleConfirmDelete,
    handleCancelDelete,
  } = useFolderDelete(onDeleteFolder, folders);

  const allSelected = folders.length > 0 && selectedFolders.length === folders.length;

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
            {/* Header with master checkbox and delete button */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={allSelected}
                  onChange={handleSelectAll}
                  aria-label="Select all folders"
                  className="w-5 h-5 cursor-pointer accent-red-500 rounded border-2 border-gray-300"
                />
                <span className="text-sm text-gray-600">
                  {allSelected ? 'all folders are selected' : 'Select all to delete'}
                </span>
              </div>
              
              <Button
                variant="primary"
                onClick={() => handleDeleteClick(selectedFolders)}
                disabled={selectedFolders.length === 0}
                className={selectedFolders.length === 0 ? 'opacity-50 cursor-not-allowed' : ''}
              >
                Delete Selected ({selectedFolders.length})
              </Button>
            </div>

            {/* Folder grid with checkboxes */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
              {folders.map((folder) => (
                <FolderCard
                  key={folder}
                  folder={folder}
                  onSelect={onSelectFolder}
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
          onConfirm={handleConfirmDelete}
          onCancel={handleCancelDelete}
        />
      )}
    </div>
  );
}

export default FoldersView;
