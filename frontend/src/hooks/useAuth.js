import { useEffect } from 'react';
import useAuthStore from '../stores/authStore';

export function useAuth(refreshFolders) {
  const {
    isLoggedIn,
    showAuthModal,
    authMode,
    authMessage,
    setIsLoggedIn,
    handleLogout,
    openAuthModal,
    closeAuthModal,
    handleAuthSuccess,
    setAuthMessage,
  } = useAuthStore();

  // Check login status on mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    const loggedIn = !!token;
    setIsLoggedIn(loggedIn);
    if (loggedIn && refreshFolders) {
      refreshFolders();
    }
  }, [refreshFolders, setIsLoggedIn]);

  const onAuthSuccess = () => {
    handleAuthSuccess();
    if (refreshFolders) {
      refreshFolders();
    }
  };

  const onLogout = () => {
    handleLogout();
    if (refreshFolders) {
      refreshFolders();
    }
  };

  return {
    isLoggedIn,
    showAuthModal,
    authMode,
    authMessage,
    handleLogout: onLogout,
    openAuthModal,
    closeAuthModal,
    handleAuthSuccess: onAuthSuccess,
    setAuthMessage,
  };
}
