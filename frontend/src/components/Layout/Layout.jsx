import React from 'react';
import { useAuth, useLayout } from '../../hooks';
import Navbar from './Navbar';
import MainContent from './MainContent';
import NotificationPanel from './NotificationPanel';

function Layout({ children }) {
  const auth = useAuth();
  const { isPanelOpen, setIsPanelOpen, togglePanel } = useLayout();

  return (
    <div className="min-h-screen bg-app-dark text-white">
      <Navbar auth={auth} togglePanel={togglePanel} />
      <MainContent>{children}</MainContent>
      <NotificationPanel isOpen={isPanelOpen} onClose={() => setIsPanelOpen(false)} />
    </div>
  );
}

export default Layout;
