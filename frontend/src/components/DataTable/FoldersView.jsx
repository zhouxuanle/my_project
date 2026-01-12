import React, { useState } from 'react';
import Button from '../ui/Button';
import FolderCard from './FolderCard';
import DeleteConfirmationModal from './DeleteConfirmationModal';
import useFolderDelete from '../../hooks/DataTable/useFolderDelete';
import { api } from '../../services/api';

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
  const [cleaning, setCleaning] = useState(false);
  const [cleanMessage, setCleanMessage] = useState('');
  
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
  } = useFolderDelete(onDeleteFolder, foldersList, onRefreshFolders);
  const allSelected = foldersList.length > 0 && selectedFolders.length === foldersList.length;

  const handleCleanFolders = async () => {
    if (selectedFolders.length === 0) {
      setCleanMessage('✗ Please select at least one folder to clean');
      return;
    }

    setCleaning(true);
    setCleanMessage('');
    
    const cleanedFolders = [];
    const failedFolders = [];
    
    try {
      // Process each selected folder sequentially
      for (const folder of selectedFolders) {
        try {
          // Fetch dataCount from metadata API
          const metadataResponse = await api.readDataMetadata(folder);
          const metadataResult = await metadataResponse.json();

          if (!metadataResult.success || !metadataResult.data.dataCount) {
            failedFolders.push({ folder, error: 'No data count found' });
            continue;
          }

          const dataCount = metadataResult.data.dataCount;
          console.log(`Cleaning folder ${folder} with dataCount ${dataCount}`);
          const response = await api.cleanData(dataCount, folder);
          const result = await response.json();
          
          if (result.success) {
            cleanedFolders.push(folder);
          } else {
            failedFolders.push({ folder, error: result.message });
          }
        } catch (error) {
          failedFolders.push({ folder, error: error.message });
        }
      }

      // Show summary message
      if (cleanedFolders.length > 0 && failedFolders.length === 0) {
        setCleanMessage(`✓ Cleaning queued for ${cleanedFolders.length} folder(s): ${cleanedFolders.join(', ')}`);
      } else if (cleanedFolders.length > 0) {
        setCleanMessage(`✓ Cleaning queued for ${cleanedFolders.length} folder(s). Failed: ${failedFolders.length}`);
      } else {
        setCleanMessage(`✗ Failed to clean any folders`);
      }
    } catch (error) {
      setCleanMessage(`✗ Error: ${error.message}`);
    } finally {
      setCleaning(false);
    }
  };

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
                  disabled={deletingFolder !== null && deletingFolder.length > 0}
                  aria-label="Select all folders"
                  className={`w-5 h-5 accent-red-500 rounded border-2 border-gray-300 ${
                    deletingFolder !== null && deletingFolder.length > 0 ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'
                  }`}
                />
                <span className="text-sm text-gray-600">
                  {allSelected ? 'all folders are selected' : 'Select folders'}
                </span>
              </div>
              
              <div className="flex gap-2">
                <Button
                  variant="action"
                  onClick={handleCleanFolders}
                  disabled={selectedFolders.length === 0 || cleaning || (deletingFolder !== null && deletingFolder.length > 0)}
                >
                  {cleaning ? 'Cleaning...' : `Clean Data (${selectedFolders.length})`}
                </Button>
                
                <Button
                  variant="primary"
                  onClick={() => handleDeleteClick(selectedFolders)}
                  disabled={selectedFolders.length === 0 || (deletingFolder !== null && deletingFolder.length > 0)}
                >
                  Delete Selected ({selectedFolders.length})
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
                  isSelected={selectedFolders.includes(folder)}
                  onToggleSelect={handleToggleFolder}
                  isDeleting={Array.isArray(deletingFolder) && deletingFolder.includes(folder)}
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
