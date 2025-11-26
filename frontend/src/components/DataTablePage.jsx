import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { useWindowWidth } from '../hooks';
import { API_ENDPOINTS } from '../constants';
import { getMaxColumns, getVisibleColumnsAndFields } from '../utils';
import { TABLE_CONFIGS } from '../config/tableConfigs';
import { ArrowDownIcon } from '../icons';
import LeftMenu from './LeftMenu';
import Button from './ui/Button';
import { TableContainer, Table, Thead, Th, Tbody, Tr, Td } from './ui/Table';

function DataTablePage() {
  const location = useLocation();
  const parentJobId = location.state?.parentJobId;
  const [loading, setLoading] = useState(true);
  const [showTable, setShowTable] = useState(true);
  const [tableData, setTableData] = useState([]);
  const [activeTable, setActiveTable] = useState('user'); // Track which table is active

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
      const response = await fetch(API_ENDPOINTS.GET_RAW_DATA(parentJobId, tableName));
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
  }, [parentJobId]);

  // Fetch data when activeTable changes
  useEffect(() => {
    fetchTableData(activeTable);
  }, [activeTable]);

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

  // Ref for the empty page
  const emptyPageRef = useRef(null);

  // Handler to scroll to empty page
  const handleArrowClick = useCallback(() => {
    if (emptyPageRef.current) {
      emptyPageRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, []);

  return (
    <div className={`App ${showTable ? 'app-with-left-menu' : ''}`}>
      {showTable && <LeftMenu showTable={showTable} setShowTable={setShowTable} />}
      
      <header className="App-header">
        <h1 className="page-title">Data Tables</h1>
        
        {showTable ? (
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
                <p>No {activeTable} data found.</p>
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

        {/* Blinking down arrow below the table-container, only when table is shown and not clipped by overflow */}
        {showTable && (
          <div className="blinking-arrow-below">
            <button
              className="blinking-arrow arrow-button-style"
              onClick={handleArrowClick}
              aria-label="Scroll to next section"
            >
              <ArrowDownIcon className="svg-block" width={40} height={40} stroke="#fff" />
            </button>
          </div>
        )}

        {/* Empty page below table-container */}
        <div ref={emptyPageRef} className="empty-page empty-page-style"></div>
      </header>
    </div>
  );
}

export default DataTablePage;