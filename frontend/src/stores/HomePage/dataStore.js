import { create } from 'zustand';

const useDataStore = create((set) => ({
  message: '',
  dataCount: 1,
  parentJobId: null,
  generating: false,
  
  // Folder state
  folders: [],
  error: null,
  hasFolder: false,

  setMessage: (value) => set({ message: value }),
  setDataCountValue: (value) => set({ dataCount: value }),
  setParentJobId: (value) => set({ parentJobId: value }),
  setGenerating: (value) => set({ generating: value }),
  
  // Folder actions
  setFolders: (folders) => set({ 
    folders, 
    hasFolder: folders.length > 0 
  }),
  setError: (error) => set({ error }),
  setHasFolder: (value) => set({ hasFolder: value }),
}));

export default useDataStore;