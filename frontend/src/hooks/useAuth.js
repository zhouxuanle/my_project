import { useEffect } from 'react';
import useAuthStore from '../stores/authStore';

export function useAuth(refreshFolders) {
  const {
    isLoggedIn,
    showAuthModal,
    authMode,
    authMessage,
    handleLogout,
    openAuthModal,
    closeAuthModal,
    handleAuthSuccess,
    setAuthMessage,
  } = useAuthStore();

  // Refresh folders on login
  useEffect(() => {
    if (isLoggedIn && refreshFolders) {
      refreshFolders();
    }
  }, [isLoggedIn, refreshFolders]);

  return {
    isLoggedIn,
    showAuthModal,
    authMode,
    authMessage,
    handleLogout,
    openAuthModal,
    closeAuthModal,
    handleAuthSuccess,
    setAuthMessage,
  };
}
