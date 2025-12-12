import { create } from 'zustand';

const useDataStore = create((set) => ({
  message: '',
  dataCount: 1,
  parentJobId: null,
  generating: false,

  setMessage: (value) => set({ message: value }),
  setDataCountValue: (value) => set({ dataCount: value }),
  setParentJobId: (value) => set({ parentJobId: value }),
  setGenerating: (value) => set({ generating: value }),
}));

export default useDataStore;