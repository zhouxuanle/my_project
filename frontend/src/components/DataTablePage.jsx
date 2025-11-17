import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import { useWindowWidth } from '../hooks';
import { API_ENDPOINTS } from '../constants';
import { getMaxColumns, getVisibleColumnsAndFields } from '../utils';
import { TABLE_CONFIGS } from '../config/tableConfigs';
import { ArrowDownIcon } from '../icons';
import LeftMenu from './LeftMenu';

function DataTablePage() {
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
      const response = await fetch(API_ENDPOINTS.GET_TABLE(tableName));
      const data = await response.json();
      if (data.success) {
        setTableData(data[tableName]);
      } else {
        console.error('Error:', data.message);
      }
    } catch (error) {
      console.error(`Error fetching ${tableName}:`, error);
    } finally {
      setLoading(false);
    }
  }, []);

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
  const tables = useMemo(() =>
    Object.entries(TABLE_CONFIGS).map(([name, config]) => ({
      name,
      label: config.label
    })),
    []
  );

  // Ref for the empty page
  const emptyPageRef = useRef(null);

  // Handler to scroll to empty page
  const handleArrowClick = useCallback(() => {
    if (emptyPageRef.current) {
      emptyPageRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, []);

  return (
    <div className="App app-with-left-menu">
      <header className="App-header">
        {/* Left fixed menu (contains Back to Home and Table List) */}
        <LeftMenu showTable={showTable} setShowTable={setShowTable} />

        {/* Only render table-container and h1 when table is shown */}
        {showTable ? (
          <>
            <h1>Data Table</h1>
            <div className="table-container">
              {/* Data Table - Hidden by default */}
              {loading ? (
                <p>Loading...</p>
              ) : tableData.length > 0 ? (
                <table className={`${activeTable}-table`}>
                  <thead>
                    <tr>
                      {visibleColumns.map((column, idx) => (
                        <th key={idx}>{column}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {tableData.map((data, index) => (
                      <tr key={data.id || index}>
                        {visibleFields.map((field, idx) => (
                          <td key={idx}>{data[field]}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p>No {activeTable} data found.</p>
              )}
            </div>
          </>
        ) : (
          <div className="center-button-container">
            {tables.map((table) => (
              <button 
                key={table.name}
                className="table-button"
                onClick={() => handleTableSelect(table.name)}
              >
                {table.label}
              </button>
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