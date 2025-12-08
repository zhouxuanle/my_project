import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { TABLE_CONFIGS } from '../config/tableConfigs';
import Button from './ui/Button';

function DataFolderDetail() {
  const { parentJobId } = useParams();
  const navigate = useNavigate();

  const tables = Object.keys(TABLE_CONFIGS).map((key) => ({
    name: key,
    label: TABLE_CONFIGS[key].label,
  }));

  return (
    <div className="center-button-container">
      <h2 className="text-lg font-semibold mb-4">Folder: {parentJobId}</h2>
      {tables.map((table) => (
        <Button
          key={table.name}
          variant="table"
          onClick={() => navigate('/user-table', { state: { parentJobId, tableName: table.name } })}
        >
          {table.label}
        </Button>
      ))}
    </div>
  );
}

export default DataFolderDetail;