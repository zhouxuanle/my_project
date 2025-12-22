import useLayoutStore from '../../stores/Layout/layoutStore';
import { useSignalR } from './useSignalR';

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

  // Initialize SignalR connection automatically
  useSignalR(addNotification);

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
