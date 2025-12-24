import React from 'react';
import Button from '../ui/Button';

function FolderTablesView({
  selectedFolder,
  tables,
  onOpenFolderTable,
  onBackToFolders,
}) {
  return (
    <div className="flex flex-col items-center w-full px-4">
      <h2 className="text-3xl font-bold mb-8">Folder: {selectedFolder}</h2>
      
      <div className="w-full max-w-2xl">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          {tables.map((table) => (
            <Button 
              key={table.name}
              variant="table"
              onClick={() => onOpenFolderTable(selectedFolder, table.name)}
            >
              {table.label}
            </Button>
          ))}
        </div>

        <div className="flex justify-center mt-8">
          <Button variant="secondary" onClick={onBackToFolders}>
            Back to folders
          </Button>
        </div>
      </div>
    </div>
  );
}

export default FolderTablesView;
