import React from 'react';
import Button from '../ui/Button';

function FolderTablesView({
  selectedFolder,
  tables,
  onOpenFolderTable,
  onBackToFolders,
}) {
  return (
    <div className="center-button-container">
      <h2 className="text-lg font-semibold mb-4">Folder: {selectedFolder}</h2>
      {tables.map((table) => (
        <Button
          key={table.name}
          variant="table"
          onClick={() => onOpenFolderTable(selectedFolder, table.name)}
        >
          {table.label}
        </Button>
      ))}
      <div style={{ marginTop: 12 }}>
        <Button variant="secondary" onClick={onBackToFolders}>Back to folders</Button>
      </div>
    </div>
  );
}

export default FolderTablesView;
