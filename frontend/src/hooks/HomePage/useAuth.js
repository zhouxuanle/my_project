import { useEffect } from 'react';
import useAuthStore from '../../stores/HomePage/authStore';

export function useAuth(refreshFolders) {
  const {
    isLoggedIn,
    showAuthModal,
    authMode,
    authMessage,
    setIsLoggedIn,
    handleLogout,
    openAuthModal,
    handleAuthSuccess,
    setAuthMessage,
  } = useAuthStore();

  // Check login status on mount and fetch folders if logged in
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
    refreshFolders();
  };

  return {
    isLoggedIn,
    showAuthModal,
    authMode,
    authMessage,
    handleLogout,
    openAuthModal,
    handleAuthSuccess: onAuthSuccess,
    setAuthMessage,
  };
}
