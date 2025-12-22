import { create } from 'zustand';

const useLayoutStore = create((set) => ({
  isPanelOpen: false,
  notifications: {
    job: [],
    error: [],
    system: []
  },
  setIsPanelOpen: (isOpen) => set({ isPanelOpen: isOpen }),
  togglePanel: () => set((state) => ({ isPanelOpen: !state.isPanelOpen })),
  addNotification: (type, notification) => set((state) => ({
    notifications: {
      ...state.notifications,
      [type]: [notification, ...state.notifications[type]]
    }
  })),
  removeNotification: (id) => set((state) => {
    const newNotifications = { ...state.notifications };
    for (const type in newNotifications) {
      newNotifications[type] = newNotifications[type].filter(n => n.id !== id);
    }
    return { notifications: newNotifications };
  }),
  clearAllNotifications: () => set({
    notifications: { job: [], error: [], system: [] }
  }),
}));

export default useLayoutStore;
