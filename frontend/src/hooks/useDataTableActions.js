import { useCallback } from 'react';
import useDataTableStore from '../stores/dataTableStore';
import { api } from '../services/api';

export default function useDataTableActions() {
  const {
    activeTable,
    setMode,
    setLoading,
    setTableData,
    setActiveTable,
    setSelectedFolder,
    setParentJobIdLocal,
    resetFolderState,
  } = useDataTableStore();

  const fetchTableData = useCallback(async ({ tableName, parentJobId }) => {
    try {
      let data;
      if (parentJobId) {
        const response = await api.getRawData(parentJobId, tableName);
        data = await response.json();
      } else {
        // Return a JSON with success evaluated to true, no API call
        data = { success: true, [tableName]: [] };
      }

      if (data.success) {
        setTableData(data[tableName] || []);
      } else {
        console.error('Error:', data.message);
        setTableData([]);
      }
    } catch (error) {
      console.error(`Error fetching ${tableName}:`, error);
      setTableData([]);
    } finally {
      setLoading(false);
    }
  }, [setLoading, setTableData]);

  const handleTableSelect = useCallback(
    (tableName, effectiveParentJobId) => {
      setTableData([]);
      setLoading(true);

      if (tableName === activeTable) {
        fetchTableData({ tableName, parentJobId: effectiveParentJobId });
        return;
      }

      setActiveTable(tableName);
    },
    [activeTable, fetchTableData, setActiveTable, setLoading, setTableData]
  );

  const openFoldersMode = useCallback(() => {
    setMode('folders');
    resetFolderState();
    setParentJobIdLocal(null);
  }, [resetFolderState, setMode, setParentJobIdLocal]);

  const selectFolder = useCallback(
    (folder) => {
      setSelectedFolder(folder);
      setMode('folderTables');
    },
    [setMode, setSelectedFolder]
  );

  const openFolderTable = useCallback(
    (folder, tableName) => {
      setParentJobIdLocal(folder);
      setActiveTable(tableName);
      setMode('tables');
      setLoading(true);
    },
    [setActiveTable, setLoading, setMode, setParentJobIdLocal]
  );

  const backToTables = useCallback(() => {
    setMode('tables');
    resetFolderState();
    setParentJobIdLocal(null);
  }, [resetFolderState, setMode, setParentJobIdLocal]);

  const backToFolders = useCallback(() => {
    setMode('folders');
    setSelectedFolder(null);
  }, [setMode, setSelectedFolder]);

  return {
    fetchTableData,
    handleTableSelect,
    openFoldersMode,
    selectFolder,
    openFolderTable,
    backToTables,
    backToFolders,
  };
}
