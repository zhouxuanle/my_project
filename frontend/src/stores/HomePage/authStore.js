import { create } from 'zustand';

const useAuthStore = create((set) => ({
  isLoggedIn: false,
  showAuthModal: false,
  authMode: 'login',
  authMessage: '',

  setIsLoggedIn: (value) => set({ isLoggedIn: value }),
  setShowAuthModal: (value) => set({ showAuthModal: value }),
  setAuthMode: (value) => set({ authMode: value }),
  setAuthMessage: (value) => set({ authMessage: value }),

  handleLogout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    set({ isLoggedIn: false, authMessage: '' });
  },

  openAuthModal: (mode = 'login') => {
    set({ authMode: mode, showAuthModal: true, authMessage: '' });
  },

  handleAuthSuccess: () => {
    set({ isLoggedIn: true, showAuthModal: false, authMessage: '' });
  },
}));

export default useAuthStore;