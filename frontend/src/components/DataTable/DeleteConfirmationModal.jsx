import React from 'react';
import Button from '../ui/Button';

function DeleteConfirmationModal({ 
  folderName, 
  error, 
  onConfirm, 
  onCancel 
}) {
  const folders = Array.isArray(folderName) ? folderName : [folderName];
  const isMultiple = folders.length > 1;

  return (
    <div 
      className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      onClick={onCancel}
    >
      <div 
        className="bg-app-dark border border-white/20 rounded-lg p-6 max-w-md w-full shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <h3 className="text-xl font-bold mb-4 text-white">
          Delete {isMultiple ? 'Folders' : 'Folder'}?
        </h3>
        <p className="text-gray-300 mb-4">
          Are you sure you want to delete {isMultiple ? 'these folders' : 'this folder'}?
        </p>
        
        <div className="mb-4 p-3 bg-black/30 rounded max-h-40 overflow-y-auto">
          <ul className="text-white text-sm space-y-1">
            {folders.map(folder => (
              <li key={folder} className="font-semibold">• {folder}</li>
            ))}
          </ul>
        </div>

        <p className="text-gray-400 text-sm mb-6">
          This will permanently delete all data in {isMultiple ? 'these folders' : 'this folder'} from Azure storage. This action cannot be undone.
        </p>
        
        {error && (
          <div className="mb-4 p-3 bg-red-500/20 border border-red-500/50 rounded text-red-300 text-sm">
            {error}
          </div>
        )}
        <div className="flex gap-3 justify-end">
          <Button
            variant="secondary"
            onClick={onCancel}
            className="px-6"
          >
            Cancel
          </Button>
          <button
            onClick={onConfirm}
            className="px-6 py-3 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg transition-colors"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}

export default DeleteConfirmationModal;
