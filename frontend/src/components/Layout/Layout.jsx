import React from 'react';
import { useAuth, useLayout } from '../../hooks';
import Navbar from './Navbar';
import MainContent from './MainContent';
import NotificationPanel from './NotificationPanel';

function Layout({ children }) {
  const auth = useAuth();
  const { 
    isPanelOpen, 
    setIsPanelOpen, 
    togglePanel, 
    notifications, 
    clearAllNotifications,
    removeNotification
  } = useLayout();

  return (
    <div className="min-h-screen bg-app-dark text-white">
      <Navbar 
        auth={auth} 
        togglePanel={togglePanel} 
        notificationCount={Object.values(notifications).flat().length} 
      />
      <MainContent>{children}</MainContent>
      <NotificationPanel 
        isOpen={isPanelOpen} 
        onClose={() => setIsPanelOpen(false)} 
        notifications={notifications}
        clearNotifications={clearAllNotifications}
        removeNotification={removeNotification}
      />
    </div>
  );
}

export default Layout;
