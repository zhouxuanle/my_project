import { useCallback } from 'react';
import useLayoutStore from '../../stores/Layout/layoutStore';
import { api } from '../../services/api';

export default function useNotificationActions() {
  const { addNotification, removeNotification, clearAllNotifications, notifications } = useLayoutStore();

  const fetchMissedNotifications = useCallback(async () => {
    try {
      const response = await api.getUnreadNotifications();
      const data = await response.json();
      
      if (data.success && data.notifications) {
        data.notifications.forEach(notif => {
          addNotification('job', {
            id: notif.id,
            message: notif.message,
            timestamp: notif.timestamp,
            status: notif.status
          });
        });
      }
    } catch (error) {
      console.error('Failed to fetch missed notifications:', error);
    }
  }, []);

  const handleRemoveNotification = useCallback(async (notif = null) => {
    if (notif) {
      // Remove single notification
      removeNotification(notif.id);
      
      try {
        await api.deleteNotification(notif.id);
      } catch (error) {
        console.error('Failed to delete notification:', error);
      }
    } else {
      // Clear all notifications
      const allNotifications = Object.values(notifications).flat();
      clearAllNotifications();
      
      const deletePromises = allNotifications.map(n => 
        api.deleteNotification(n.id).catch(error => {
          console.error(`Failed to delete notification ${n.id}:`, error);
        })
      );
      
      await Promise.all(deletePromises);
    }
  }, [notifications]);

  return {
    fetchMissedNotifications,
    handleRemoveNotification,
  };
}
