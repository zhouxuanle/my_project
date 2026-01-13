import React from 'react';
import Button from '../ui/Button';
import FolderCard from './FolderCard';
import DeleteConfirmationModal from './DeleteConfirmationModal';
import useFolderDelete from '../../hooks/DataTable/useFolderDelete';
import useDataTableActions from '../../hooks/DataTable/useDataTableActions';

function FoldersView({
  foldersLoading,
  foldersError,
  folders = [],
  onSelectFolder,
  onBackToTables,
  onDeleteFolder,
  onRefreshFolders,
}) {
  // Ensure folders is always an array
  const foldersList = Array.isArray(folders) ? folders : [];
  
  const {
    selectedFolders,
    isDeleting,
    confirmDelete,
    deleteError,
    handleToggleFolder,
    handleSelectAll,
    handleDeleteClick,
    handleConfirmDelete,
    handleCancelDelete,
  } = useFolderDelete(onDeleteFolder, foldersList, onRefreshFolders);

  const { handleCleanFolders, cleaning, cleanMessage } = useDataTableActions();
  const allSelected = foldersList.length > 0 && selectedFolders.length === foldersList.length;

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
        
        {!foldersLoading && !foldersError && foldersList.length === 0 && (
          <div className="text-gray-400 text-center py-8">No folders found.</div>
        )}

        {!foldersLoading && !foldersError && foldersList.length > 0 && (
          <>
            {/* Header with master checkbox and action buttons */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={allSelected}
                  onChange={handleSelectAll}
                  disabled={isDeleting || cleaning}
                  aria-label="Select all folders"
                  className={`w-5 h-5 accent-red-500 rounded border-2 border-gray-300 ${
                    isDeleting || cleaning ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'
                  }`}
                />
                <span className="text-sm text-gray-600">
                  {allSelected ? 'all folders are selected' : 'Select folders'}
                </span>
              </div>
              
              <div className="flex gap-2">
                <Button
                  variant="primary"
                  onClick={() => handleCleanFolders(selectedFolders)}
                  disabled={selectedFolders.length === 0 || cleaning || isDeleting}
                  className="text-sm font-bold italic"
                >
                  {cleaning ? 'Cleaning...' : `Clean Data (${selectedFolders.length})`}
                </Button>
                
                <Button
                  variant="primary"
                  onClick={() => handleDeleteClick(selectedFolders)}
                  disabled={selectedFolders.length === 0 || cleaning || isDeleting}
                  className="text-sm font-bold italic text-red-600"
                >
                  {isDeleting ? 'Deleting...' : `Delete Selected (${selectedFolders.length})`}
                </Button>
              </div>
            </div>

            {/* Folder grid with checkboxes */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
              {foldersList.map((folder) => (
                <FolderCard
                  key={folder}
                  folder={folder}
                  onSelect={onSelectFolder}
                  checked={selectedFolders.includes(folder)}
                  onToggleSelect={handleToggleFolder}
                  disabled={isDeleting && selectedFolders.includes(folder)}
                />
              ))}
            </div>

            {/* Clean message feedback */}
            {cleanMessage && (
              <div className="mt-6 flex flex-col items-center gap-3">
                <p className={`text-sm ${
                  cleanMessage.startsWith('✓') ? 'text-green-400' : 'text-red-400'
                }`}>
                  {cleanMessage}
                </p>
              </div>
            )}
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
