import React from 'react';
import { useNavigate } from 'react-router-dom';
import { TableIcon, HomeIcon, DataIcon } from '../icons';
import MenuButton from './ui/MenuButton';

// Left-side menu component: fixed vertical menu with two buttons
function LeftMenu({ showTable, setShowTable }) {
  const navigate = useNavigate();

  return (
    <nav className="left-menu" aria-label="Primary">
      <MenuButton
        variant="small"
        onClick={() => setShowTable(prev => !prev)}
        aria-pressed={showTable}
        title="Table List"
      >
        <TableIcon className="menu-icon" width={28} height={28} aria-hidden />
      </MenuButton>
      <div className="menu-label">Tables</div>

      <MenuButton
        variant="small"
        onClick={() => navigate('/data')}
        title="Data"
      >
        <DataIcon className="menu-icon" width={24} height={24} aria-hidden />
      </MenuButton>
      <div className="menu-label">Data</div>

      <MenuButton
        variant="small"
        onClick={() => navigate('/')}
        title="Back to Home"
      >
        <HomeIcon className="menu-icon" width={22} height={22} aria-hidden />
      </MenuButton>
      <div className="menu-label">Home</div>
    </nav>
  );
}

export default LeftMenu;