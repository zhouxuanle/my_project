import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../ui/Button';

function ViewTableButton({ showViewTableButton, parentJobId, setHasViewedTable }) {
  const navigate = useNavigate();

  if (!showViewTableButton) return null;

  return (
    <Button
      variant="primary"
      onClick={() => {
        setHasViewedTable(true);
        navigate('/user-table', { state: { parentJobId } });
      }}
    >
      <span>View Data Table →</span>
    </Button>
  );
}

export default ViewTableButton;