import React from 'react';
import Button from '../ui/Button';

function TablesMenuView({ tables, onSelectTable }) {
  return (
    <div className="center-button-container">
      {tables.map((table) => (
        <Button
          key={table.name}
          variant="table"
          onClick={() => onSelectTable(table.name)}
        >
          {table.label}
        </Button>
      ))}
    </div>
  );
}

export default TablesMenuView;
