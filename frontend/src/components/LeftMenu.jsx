import React from 'react';
import { useNavigate } from 'react-router-dom';
import { TableIcon, HomeIcon } from '../icons';

// Left-side menu component: fixed vertical menu with two buttons
function LeftMenu({ showTable, setShowTable }) {
  const navigate = useNavigate();

  return (
    <nav className="left-menu" aria-label="Primary">
      <button
        className="menu-small"
        onClick={() => setShowTable(prev => !prev)}
        aria-pressed={showTable}
        title="Table List"
      >
        <TableIcon className="menu-icon" width={28} height={28} aria-hidden />
      </button>
      <div className="menu-label">Tables</div>

      <button
        className="menu-small"
        onClick={() => navigate('/')}
        title="Back to Home"
      >
        <HomeIcon className="menu-icon" width={22} height={22} aria-hidden />
      </button>
      <div className="menu-label">Home</div>
    </nav>
  );
}

export default LeftMenu;