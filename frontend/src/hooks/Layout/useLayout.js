import { useEffect } from 'react';
import useLayoutStore from '../../stores/Layout/layoutStore';
import useAuthStore from '../../stores/authStore';
import { useSignalR } from './useSignalR';
import useNotificationActions from './useNotificationActions';

export function useLayout() {
  const { 
    isPanelOpen, 
    setIsPanelOpen, 
    togglePanel, 
    notifications, 
    addNotification, 
    removeNotification,
    clearAllNotifications
  } = useLayoutStore();

  const { isLoggedIn } = useAuthStore();
  const { fetchMissedNotifications } = useNotificationActions();

  // Initialize SignalR connection automatically
  useSignalR(addNotification);

  // Fetch missed notifications on login
  useEffect(() => {
    if (isLoggedIn) {
      fetchMissedNotifications();
      console.log('Fetched missed notifications on login');
    }
  }, [isLoggedIn]);

  return {
    isPanelOpen,
    setIsPanelOpen,
    togglePanel,
    notifications,
    addNotification,
    removeNotification,
    clearAllNotifications,
  };
}
