import React from 'react';
import Button from '../ui/Button';

function FolderCard({ folder, onSelect, isSelected, onToggleSelect, isDeleting }) {
  return (
    <div className="flex items-center gap-3">
      <input
        type="checkbox"
        checked={isSelected}
        onChange={() => onToggleSelect(folder)}
        disabled={isDeleting}
        aria-label={`Select folder ${folder}`}
        className="w-5 h-5 cursor-pointer accent-red-500 rounded border-2 border-gray-300"
      />
      
      <Button
        variant="table"
        onClick={() => onSelect(folder)}
        disabled={isDeleting}
      >
        {folder}
      </Button>
    </div>
  );
}

export default FolderCard;
