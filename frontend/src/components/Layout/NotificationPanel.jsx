import React from 'react';
import useNotificationActions from '../../hooks/Layout/useNotificationActions';

function NotificationPanel({ isOpen, onClose, notifications }) {
  // Flatten notifications from all categories into a single array for display
  const allNotifications = Object.values(notifications).flat();
  const { handleRemoveNotification } = useNotificationActions();
  
  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={onClose}
        />
      )}

      {/* Panel */}
      <div
        className={`fixed top-0 right-0 h-full w-80 bg-app-dark text-white shadow-lg z-50 transform transition-transform duration-300 ${
          isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">Notifications</h2>
              <div className="flex space-x-2">
                {allNotifications.length > 0 && (
                  <button
                    onClick={() => handleRemoveNotification()}
                    className="text-xs text-gray-400 hover:text-white"
                  >
                    Clear All
                  </button>
                )}
                <button
                  onClick={onClose}
                  className="text-white hover:text-gray-300 focus:outline-none"
                >
                  ✕
                </button>
              </div>
            </div>
        <div className="p-4 overflow-y-auto h-[calc(100%-4rem)]">
          {allNotifications.length === 0 ? (
            <p className="text-gray-300">No new notifications.</p>
          ) : (
            <div className="space-y-3">
              {allNotifications.map((notif) => (
                <div key={notif.id} className="p-3 bg-app-hover rounded-lg border border-app-hover relative">
                  <button
                    onClick={() => handleRemoveNotification(notif)}
                    className="absolute top-2 right-2 text-gray-400 hover:text-white focus:outline-none"
                    aria-label="Close notification"
                  >
                    ✕
                  </button>
                  <p className="text-sm text-white pr-6">{notif.message}</p>
                  <p className="text-xs text-gray-400 mt-1">
                    {new Date(notif.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default NotificationPanel;
