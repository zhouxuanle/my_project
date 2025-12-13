import { useEffect } from 'react';
import useDataTableStore from '../stores/dataTableStore';

export default function useDataTableEffects({
  locationState,
  locationKey,
  effectiveParentJobId,
  fetchTableData,
}) {
  const {
    mode,
    activeTable,
    setLoading,
    setTableData,
    initFromLocation,
  } = useDataTableStore();

  // Keep behavior: allow navigating to the same route with state (openFolders/tableName)
  useEffect(() => {
    initFromLocation({
      tableName: locationState?.tableName,
      openFolders: locationState?.openFolders,
    });

    // When opening folders view via navigation, match original resets.
    if (locationState?.openFolders) {
      setTableData([]);
      setLoading(false);
    }
  }, [
    initFromLocation,
    locationState?.openFolders,
    locationState?.tableName,
    locationKey,
    setLoading,
    setTableData,
  ]);

  // Fetch data when activeTable changes (tables mode only)
  useEffect(() => {
    if (mode === 'tables') {
      fetchTableData({ tableName: activeTable, parentJobId: effectiveParentJobId });
    }
  }, [activeTable, effectiveParentJobId, fetchTableData, mode]);
}
