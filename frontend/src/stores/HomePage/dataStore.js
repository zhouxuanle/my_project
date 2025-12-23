import { create } from 'zustand';

const useDataStore = create((set) => ({
  message: '',
  dataCount: 1,
  parentJobId: null,
  generating: false,
  hasFolder: false,

  setMessage: (value) => set({ message: value }),
  setDataCountValue: (value) => set({ dataCount: value }),
  setParentJobId: (value) => set({ parentJobId: value }),
  setGenerating: (value) => set({ generating: value }),
  setHasFolder: (value) => set({ hasFolder: value }),
}));

export default useDataStore;