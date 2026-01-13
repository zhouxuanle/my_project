import { useCallback, useState } from 'react';
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
    // resetFolderState,
  } = useDataTableStore();
  const [cleaning, setCleaning] = useState(false);
  const [cleanMessage, setCleanMessage] = useState('');

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
    // resetFolderState();
  }, []);

  const backToFolders = useCallback(() => {
    setMode('folders');
    setSelectedFolder(null);
  }, []);

  const handleCleanFolders = useCallback(
    async (selectedFolders) => {
      if (selectedFolders.length === 0) {
        setCleanMessage('✗ Please select at least one folder to clean');
        return;
      }

      setCleaning(true);
      setCleanMessage('');

      const cleanedFolders = [];
      const failedFolders = [];

      try {
        // Process each selected folder sequentially
        for (const folder of selectedFolders) {
          try {
            // Fetch dataCount from metadata API
            const metadataResponse = await api.readDataMetadata(folder);
            const metadataResult = await metadataResponse.json();

            if (!metadataResult.success || !metadataResult.data.dataCount) {
              failedFolders.push({ folder, error: 'No data count found' });
              continue;
            }

            const dataCount = metadataResult.data.dataCount;
            console.log(`Cleaning folder ${folder} with dataCount ${dataCount}`);
            const response = await api.cleanData(dataCount, folder);
            const result = await response.json();

            if (result.success) {
              cleanedFolders.push(folder);
            } else {
              failedFolders.push({ folder, error: result.message });
            }
          } catch (error) {
            failedFolders.push({ folder, error: error.message });
          }
        }

        // Show summary message
        if (cleanedFolders.length > 0 && failedFolders.length === 0) {
          setCleanMessage(
            `✓ Cleaning queued for ${cleanedFolders.length} folder(s): ${cleanedFolders.join(', ')}`
          );
        } else if (cleanedFolders.length > 0) {
          setCleanMessage(
            `✓ Cleaning queued for ${cleanedFolders.length} folder(s). Failed: ${failedFolders.length}`
          );
        } else {
          setCleanMessage(`✗ Failed to clean any folders`);
        }
      } catch (error) {
        setCleanMessage(`✗ Error: ${error.message}`);
      } finally {
        setCleaning(false);
      }
    },
    []
  );

  return {
    fetchTableData,
    selectFolder,
    openFolderTable,
    backToTables,
    backToFolders,
    handleCleanFolders,
    cleaning,
    cleanMessage,
  };
}
