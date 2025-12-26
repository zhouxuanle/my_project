import { useCallback } from 'react';
import useDataTableStore from '../../stores/DataTable/dataTableStore';
import { api } from '../../services/api';

export default function useDataTableActions() {
  const {
    tableData,
    setMode,
    setLoading,
    setTableData,
    setActiveTable,
    setSelectedFolder,
    setParentJobIdLocal,
    resetFolderState,
  } = useDataTableStore();

  const fetchTableData = useCallback(async ({ tableName, parentJobId }) => {
    setLoading(true);
    try {
      let data;
      if (parentJobId && tableName) {
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
      setMode('');
    }
  }, []); // Empty deps - all setters are stable from Zustand

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
    },
    []
  );

  const backToTables = useCallback(() => {
    setMode('tables');
    resetFolderState();
  }, []);

  const backToFolders = useCallback(() => {
    setMode('folders');
    setSelectedFolder(null);
  }, []);

  return {
    fetchTableData,
    selectFolder,
    openFolderTable,
    backToTables,
    backToFolders,
  };
}
