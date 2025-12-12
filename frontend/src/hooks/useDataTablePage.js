import { useMemo } from 'react';
import useDataTableStore from '../stores/dataTableStore';
import { TABLE_CONFIGS, TABLE_LIST } from '../config/tableConfigs';
import useDataTableActions from './useDataTableActions';
import useDataTableEffects from './useDataTableEffects';

export default function useDataTablePage({
  locationState,
  locationParentJobId,
  locationKey,
} = {}) {
  const {
    mode,
    loading,
    showTable,
    tableData,
    activeTable,
    selectedFolder,
    parentJobIdLocal,
  } = useDataTableStore();

  const effectiveParentJobId = locationParentJobId || parentJobIdLocal || null;

  const {
    fetchTableData,
    handleTableSelect,
    openFoldersMode,
    selectFolder,
    openFolderTable,
    backToTables,
    backToFolders,
  } = useDataTableActions();

  useDataTableEffects({
    locationState,
    locationKey,
    effectiveParentJobId,
    fetchTableData,
  });

  const currentTableConfig = useMemo(
    () => TABLE_CONFIGS[activeTable],
    [activeTable]
  );

  return {
    // state
    mode,
    loading,
    showTable,
    tableData,
    activeTable,
    selectedFolder,
    effectiveParentJobId,

    // derived
    tables: TABLE_LIST,
    currentTableConfig,

    // actions
    handleTableSelect: (tableName) => handleTableSelect(tableName, effectiveParentJobId),
    openFoldersMode,
    selectFolder,
    openFolderTable,
    backToTables,
    backToFolders,
  };
}
