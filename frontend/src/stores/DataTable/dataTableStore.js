import { create } from 'zustand';

const DEFAULT_ACTIVE_TABLE = 'user';

const useDataTableStore = create((set) => ({
  // UI state
  mode: 'tables', // 'tables' | 'folders' | 'folderTables'
  loading: true,

  // Data state
  tableData: [],
  activeTable: DEFAULT_ACTIVE_TABLE,

  // Folder navigation state
  selectedFolder: null,
  parentJobIdLocal: null,

  // Simple setters
  setMode: (mode) => set({ mode }),
  setLoading: (loading) => set({ loading }),
  setTableData: (tableData) => set({ tableData }),
  setActiveTable: (activeTable) => set({ activeTable }),
  setSelectedFolder: (selectedFolder) => set({ selectedFolder }),
  setParentJobIdLocal: (parentJobIdLocal) => set({ parentJobIdLocal }),

  // Helpers
  resetFolderState: () => set({ selectedFolder: null, parentJobIdLocal: null }),
}));

export default useDataTableStore;
