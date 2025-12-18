import React from 'react';

function NotificationPanel({ isOpen, onClose }) {
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
        className={`fixed top-0 left-0 h-full w-80 bg-app-dark text-white shadow-lg z-50 transform transition-transform duration-300 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="p-4 border-b border-app-hover">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold">Notifications</h2>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-300 focus:outline-none"
            >
              ✕
            </button>
          </div>
        </div>
        <div className="p-4">
          {/* Placeholder for notifications */}
          <p className="text-gray-300">No new notifications.</p>
          {/* Add notification items here */}
        </div>
      </div>
    </>
  );
}

export default NotificationPanel;
