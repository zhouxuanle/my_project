import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { useWindowWidth, useDataFolders } from '../hooks';
import { api } from '../services/api';
import { getMaxColumns, getVisibleColumnsAndFields } from '../utils';
import { TABLE_CONFIGS } from '../config/tableConfigs';
// Arrow-down UI removed — no icon import needed
import LeftMenu from './LeftMenu';
import Button from './ui/Button';
import { TableContainer, Table, Thead, Th, Tbody, Tr, Td } from './ui/Table';

function DataTablePage() {
  const location = useLocation();
  const locationParentJobId = location.state?.parentJobId;
  const initialMode = location.state?.openFolders ? 'folders' : 'tables';
  
  const [mode, setMode] = useState(initialMode); // 'tables' | 'folders' | 'folderTables'
  const [loading, setLoading] = useState(true);
  const [showTable, setShowTable] = useState(true);
  const [tableData, setTableData] = useState([]);
  const [activeTable, setActiveTable] = useState(() => {
    // If navigated with a tableName in state, use it as initial active table
    return location.state?.tableName || 'user';
  }); // Track which table is active
  
  // Folder-related state
  const [selectedFolder, setSelectedFolder] = useState(null);
  const [parentJobIdLocal, setParentJobIdLocal] = useState(null);
  const effectiveParentJobId = locationParentJobId || parentJobIdLocal || null;
  
  const { folders, loading: foldersLoading, error: foldersError } = useDataFolders({ autoFetch: true });

  // Memoize table config for current active table
  const currentTableConfig = useMemo(() => TABLE_CONFIGS[activeTable], [activeTable]);

  // Responsive: determine how many columns to show based on window width
  const windowWidth = useWindowWidth();
  
  // Calculate visible columns and fields with responsive behavior
  const { visibleColumns, visibleFields } = useMemo(() => {
    const maxColumns = getMaxColumns(windowWidth, currentTableConfig.columns.length);
    return getVisibleColumnsAndFields(currentTableConfig, maxColumns);
  }, [windowWidth, currentTableConfig]);

  // Generic fetch function with useCallback for optimization
  // Fetch table data from backend
  const fetchTableData = useCallback(async (tableName) => {
    try {
      let response;
      if (effectiveParentJobId) {
        response = await api.getRawData(effectiveParentJobId, tableName);
      } else {
        response = await api.getTableData(tableName);
      }
      
      const data = await response.json();
      if (data.success) {
        setTableData(data[tableName]);
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
  }, [effectiveParentJobId]);

  // Watch for location state changes (when navigating to same route with different state)
  useEffect(() => {
    if (location.state?.openFolders) {
      setMode('folders');
      setSelectedFolder(null);
      setParentJobIdLocal(null);
    }
  }, [location.state]);

  // Fetch data when activeTable changes
  useEffect(() => {
    if (mode === 'tables') {
      fetchTableData(activeTable);
    }
  }, [activeTable, mode, fetchTableData]);

  // Handler for table selection
  const handleTableSelect = useCallback((tableName) => {
    setTableData([]);
    setLoading(true);
    setShowTable(true);
    if (tableName === activeTable) {
      fetchTableData(tableName);
    }
    setActiveTable(tableName);
  }, [activeTable, fetchTableData]);

  // Memoize tables array from config
  const tables = Object.keys(TABLE_CONFIGS).map(key => ({
    name: key,
    label: TABLE_CONFIGS[key].label
  }));

  // (Blinking arrow feature removed)

  return (
    <div className={`App ${showTable ? 'app-with-left-menu' : ''}`}>
      {showTable && <LeftMenu />}
      
      <header className="App-header">
        <h1 className="page-title">Data Tables</h1>
        
        {mode === 'folders' ? (
          <div className="center-button-container">
            <h2 className="text-lg font-semibold mb-4">Your Data Folders</h2>
            {foldersLoading && <div>Loading...</div>}
            {foldersError && <div className="text-red-500">{foldersError.message || 'Failed to fetch folders'}</div>}
            {!foldersLoading && !foldersError && folders.length === 0 && <div>No folders found.</div>}
            {!foldersLoading && !foldersError && folders.map((folder) => (
              <Button
                key={folder}
                variant="table"
                onClick={() => { setSelectedFolder(folder); setMode('folderTables'); }}
              >
                {folder}
              </Button>
            ))}
            <div style={{ marginTop: 12 }}>
              <Button variant="secondary" onClick={() => { setMode('tables'); setSelectedFolder(null); setParentJobIdLocal(null); }}>Back to tables</Button>
            </div>
          </div>
        ) : mode === 'folderTables' && selectedFolder ? (
          <div className="center-button-container">
            <h2 className="text-lg font-semibold mb-4">Folder: {selectedFolder}</h2>
            {tables.map((table) => (
              <Button
                key={table.name}
                variant="table"
                onClick={() => {
                  setParentJobIdLocal(selectedFolder);
                  setActiveTable(table.name);
                  setMode('tables');
                  setShowTable(true);
                  setLoading(true);
                }}
              >
                {table.label}
              </Button>
            ))}
            <div style={{ marginTop: 12 }}>
              <Button variant="secondary" onClick={() => { setMode('folders'); setSelectedFolder(null); }}>Back to folders</Button>
            </div>
          </div>
        ) : showTable ? (
          <>
            <TableContainer>
              {tableData.length > 0 ? (
                <Table>
                  <Thead>
                    <Tr>
                      {visibleColumns.map((col, index) => (
                        <Th key={index}>{col}</Th>
                      ))}
                    </Tr>
                  </Thead>
                  <Tbody>
                    {tableData.map((data, index) => (
                      <Tr key={data.id || index}>
                        {visibleFields.map((field, idx) => (
                          <Td key={idx}>{data[field]}</Td>
                        ))}
                      </Tr>
                    ))}
                  </Tbody>
                </Table>
              ) : (
                <p>No {activeTable} data found. {effectiveParentJobId ? '' : 'Use the Data button to view generated data folders.'}</p>
              )}
            </TableContainer>
          </>
        ) : (
          <div className="center-button-container">
            {tables.map((table) => (
              <Button 
                key={table.name}
                variant="table"
                onClick={() => handleTableSelect(table.name)}
              >
                {table.label}
              </Button>
            ))}
          </div>
        )}

        {/* Blinking arrow removed intentionally. */}

        {/* Empty page below table-container */}
        <div className="empty-page empty-page-style"></div>
      </header>
    </div>
  );
}

export default DataTablePage;