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

  // Check login status on mount
  useEffect(() => {
    if (isLoggedIn && refreshFolders) {
      refreshFolders();
    }
  }, [isLoggedIn,refreshFolders]);

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
