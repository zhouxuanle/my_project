import React from 'react';
import Button from '../ui/Button';

function FoldersView({
  foldersLoading,
  foldersError,
  folders,
  onSelectFolder,
  onBackToTables,
}) {
  return (
    <div className="center-button-container">
      <h2 className="text-lg font-semibold mb-4">Your Data Folders</h2>
      {foldersLoading && <div>Loading...</div>}
      {foldersError && <div className="text-red-500">{foldersError.message || 'Failed to fetch folders'}</div>}
      {!foldersLoading && !foldersError && folders.length === 0 && <div>No folders found.</div>}
      {!foldersLoading && !foldersError && folders.map((folder) => (
        <Button
          key={folder}
          variant="table"
          onClick={() => onSelectFolder(folder)}
        >
          {folder}
        </Button>
      ))}
      <div style={{ marginTop: 12 }}>
        <Button variant="secondary" onClick={onBackToTables}>Back to tables</Button>
      </div>
    </div>
  );
}

export default FoldersView;
