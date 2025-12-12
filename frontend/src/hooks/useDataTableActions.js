import { useCallback } from 'react';
import useDataTableStore from '../stores/dataTableStore';
import { api } from '../services/api';

export default function useDataTableActions() {
  const {
    activeTable,
    setMode,
    setLoading,
    setShowTable,
    setTableData,
    setActiveTable,
    setSelectedFolder,
    setParentJobIdLocal,
    resetFolderState,
  } = useDataTableStore();

  const fetchTableData = useCallback(async ({ tableName, parentJobId }) => {
    try {
      let response;
      if (parentJobId) {
        response = await api.getRawData(parentJobId, tableName);
      } else {
        response = await api.getTableData(tableName);
      }

      const data = await response.json();
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
      setShowTable(true);

      if (tableName === activeTable) {
        fetchTableData({ tableName, parentJobId: effectiveParentJobId });
        return;
      }

      setActiveTable(tableName);
    },
    [activeTable, fetchTableData, setActiveTable, setLoading, setShowTable, setTableData]
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
      setShowTable(true);
      setLoading(true);
    },
    [setActiveTable, setLoading, setMode, setParentJobIdLocal, setShowTable]
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
