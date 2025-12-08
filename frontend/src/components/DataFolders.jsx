import React from 'react';
import { useNavigate } from 'react-router-dom';
import useDataFolders from '../hooks/useDataFolders';
import Panel from './ui/Panel';
import Button from './ui/Button';

function DataFolders() {
  const navigate = useNavigate();
  const { folders, loading, error, refresh } = useDataFolders({ autoFetch: true });

  return (
    <div className="center-button-container">
      <h2 className="text-lg font-semibold mb-4">Your Data Folders</h2>
      {loading && <div>Loading...</div>}
      {error && <div className="text-red-500">{error.message || 'Failed to fetch folders'}</div>}
      {!loading && !error && folders.length === 0 && <div>No folders found.</div>}
      {!loading && !error && folders.map((folder) => (
        <Button
          key={folder}
          variant="table"
          onClick={() => navigate(`/data/${folder}`)}
        >
          {folder}
        </Button>
      ))}
    </div>
  );
}

export default DataFolders;
