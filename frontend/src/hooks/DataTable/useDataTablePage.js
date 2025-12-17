import { useMemo, useEffect } from 'react';
import useDataTableStore from '../../stores/DataTable/dataTableStore';
import { TABLE_CONFIGS, TABLE_LIST } from '../../config/tableConfigs';
import useDataTableActions from './useDataTableActions';

export default function useDataTablePage({
  locationState,
  locationParentJobId,
  locationKey,
} = {}) {
  const {
    mode,
    tableData,
    activeTable,
    selectedFolder,
    parentJobIdLocal,
    loading,
    setMode,
    resetFolderState,
  } = useDataTableStore();

  const effectiveParentJobId = locationParentJobId || parentJobIdLocal || null;

  const {
    fetchTableData,
    selectFolder,
    openFolderTable,
    backToTables,
    backToFolders,
  } = useDataTableActions();

  // Keep behavior: allow navigating to the same route with state (openFolders)
  useEffect(() => {
    if (locationState?.openFolders) {
      setMode('folders');
      resetFolderState();
    }
  }, [
    locationState?.openFolders,
    locationKey,
  ]);

  // Fetch data when activeTable changes (tables mode only)
  useEffect(() => {
    if (mode === 'tables') {
      fetchTableData({ tableName: activeTable, parentJobId: effectiveParentJobId });
    }
  }, [activeTable, effectiveParentJobId, fetchTableData, mode]);

  const currentTableConfig = useMemo(
    () => TABLE_CONFIGS[activeTable],
    [activeTable]
  );

  return {
    // state
    mode,
    tableData,
    activeTable,
    selectedFolder,
    effectiveParentJobId,
    loading,

    // derived
    tables: TABLE_LIST,
    currentTableConfig,

    // actions
    selectFolder,
    openFolderTable,
    backToTables,
    backToFolders,
  };
}
