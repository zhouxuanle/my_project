import { create } from 'zustand';

const useLayoutStore = create((set) => ({
  isPanelOpen: false,
  setIsPanelOpen: (isOpen) => set({ isPanelOpen: isOpen }),
  togglePanel: () => set((state) => ({ isPanelOpen: !state.isPanelOpen })),
}));

export default useLayoutStore;
