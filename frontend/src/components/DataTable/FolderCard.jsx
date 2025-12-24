import React from 'react';
import Button from '../ui/Button';

function FolderCard({ folder, onSelect, isDeleteMode, isSelected, onToggleSelect, isDeleting }) {
  const handleClick = () => {
    if (isDeleteMode) {
      onToggleSelect(folder);
    } else {
      onSelect(folder);
    }
  };

  return (
    <div className="relative">
      <Button
        variant="table"
        onClick={handleClick}
        disabled={isDeleting}
        className={`${isDeleting ? 'opacity-50' : ''} ${isDeleteMode && isSelected ? 'ring-2 ring-red-500' : ''}`}
      >
        {folder}
      </Button>
      {isDeleteMode && (
        <div className="absolute -top-2 -right-2 z-10">
          <input
            type="checkbox"
            checked={isSelected}
            onChange={() => onToggleSelect(folder)}
            disabled={isDeleting}
            aria-label={`Select folder ${folder}`}
            className="w-6 h-6 cursor-pointer accent-red-500 rounded border-2 border-white shadow-lg"
          />
        </div>
      )}
    </div>
  );
}

export default FolderCard;
