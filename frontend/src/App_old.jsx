import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import { TableIcon, HomeIcon, ArrowDownIcon } from './icons';
import './App.css'; // For basic styling

// API endpoint constants
const API_BASE_URL = 'http://127.0.0.1:5000';
const API_ENDPOINTS = {
  WRITE_TO_DB: `${API_BASE_URL}/write_to_db`,
  GET_TABLE: (tableName) => `${API_BASE_URL}/get_${tableName}`
};

// Input validation constants
const DATA_COUNT_LIMITS = {
  MIN: 1,
  MAX: 999999
};

// Responsive breakpoint constants
const BREAKPOINTS = {
  SMALL: 600,
  MEDIUM: 700,
  LARGE: 900
};

// Utility function to calculate max columns based on window width
function getMaxColumns(windowWidth, totalColumns) {
  if (windowWidth < BREAKPOINTS.SMALL) {
    return Math.max(2, totalColumns - 6);
  } else if (windowWidth < BREAKPOINTS.MEDIUM) {
    return Math.max(3, totalColumns - 4);
  } else if (windowWidth < BREAKPOINTS.LARGE) {
    return Math.max(4, totalColumns - 3);
  }
  return totalColumns;
}

// Utility function to get visible columns/fields with created_at always at the end
function getVisibleColumnsAndFields(config, maxColumns) {
  const { columns, fields } = config;
  const createdAtIndex = fields.indexOf('created_at');
  
  if (createdAtIndex === -1) {
    // No created_at column, just slice normally
    return {
      visibleColumns: columns.slice(0, maxColumns),
      visibleFields: fields.slice(0, maxColumns)
    };
  }
  
  // Remove created_at from arrays temporarily
  const columnsWithoutCreatedAt = columns.filter((_, idx) => idx !== createdAtIndex);
  const fieldsWithoutCreatedAt = fields.filter(field => field !== 'created_at');
  
  // Take up to maxColumns-1 items, then add created_at at the end
  const numToTake = Math.max(1, maxColumns - 1);
  const slicedColumns = columnsWithoutCreatedAt.slice(0, numToTake);
  const slicedFields = fieldsWithoutCreatedAt.slice(0, numToTake);
  
  return {
    visibleColumns: [...slicedColumns, columns[createdAtIndex]],
    visibleFields: [...slicedFields, 'created_at']
  };
}

// Custom hook for typewriter effect
function useTypewriterEffect(text, speed = 50) {
  const [displayedText, setDisplayedText] = useState('');

  useEffect(() => {
    if (text) {
      setDisplayedText('');
      let index = 0;
      const timer = setInterval(() => {
        if (index < text.length) {
          let message_letter = text[index];
          setDisplayedText(prev => prev + message_letter);
          index++;
        } else {
          clearInterval(timer);
        }
      }, speed);
      return () => clearInterval(timer);
    }
  }, [text, speed]);

  return displayedText;
}

// Responsive hook to get window width
function useWindowWidth() {
  const [width, setWidth] = useState(window.innerWidth);
  useEffect(() => {
    function handleResize() {
      setWidth(window.innerWidth);
    }
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  return width;
}

// Utility function for input validation
function validateDataCount(value) {
  return Math.max(DATA_COUNT_LIMITS.MIN, Math.min(DATA_COUNT_LIMITS.MAX, Number(value)));
}

// Table configuration to eliminate code duplication
const TABLE_CONFIGS = {
  user: {
    label: 'User Table',
    columns: ['ID', 'Username', 'Real Name', 'Email', 'Phone', 'Sex', 'Age', 'Job', 'created_at'],
    fields: ['id', 'user_name', 'real_name', 'email', 'phone_number', 'sex', 'age', 'job', 'created_at']
  },
  address: {
    label: 'Address Table',
    columns: ['ID', 'User ID', 'Title', 'Address Line', 'Country', 'City', 'Postal Code', 'created_at'],
    fields: ['id', 'user_id', 'title', 'address_line', 'country', 'city', 'postal_code', 'created_at']
  },
  category: {
    label: 'Category Table',
    columns: ['ID', 'Name', 'Description', 'created_at'],
    fields: ['id', 'name', 'description', 'created_at']
  },
  subcategory: {
    label: 'Subcategory Table',
    columns: ['ID', 'Parent ID', 'Name', 'Description', 'created_at'],
    fields: ['id', 'parent_id', 'name', 'description', 'created_at']
  },
  product: {
    label: 'Product Table',
    columns: ['ID', 'Name', 'Description', 'Category ID', 'created_at'],
    fields: ['id', 'name', 'description', 'category_id', 'created_at']
  },
  products_sku: {
    label: 'Products SKU Table',
    columns: ['ID', 'Product ID', 'Price', 'Stock', 'created_at'],
    fields: ['id', 'product_id', 'price', 'stock', 'created_at']
  },
  wishlist: {
    label: 'Wishlist Table',
    columns: ['ID', 'User ID', 'Product SKU ID', 'created_at'],
    fields: ['id', 'user_id', 'products_sku_id', 'created_at']
  },
  payment: {
    label: 'Payment Table',
    columns: ['ID', 'Amount', 'Provider', 'Status', 'created_at'],
    fields: ['id', 'amount', 'provider', 'status', 'created_at']
  },
  order: {
    label: 'Order Table',
    columns: ['ID', 'User ID', 'Payment ID', 'created_at'],
    fields: ['id', 'user_id', 'payment_id', 'created_at']
  },
  order_item: {
    label: 'Order Item Table',
    columns: ['ID', 'Order ID', 'Product SKU ID', 'Quantity', 'created_at'],
    fields: ['id', 'order_id', 'products_sku_id', 'quantity', 'created_at']
  },
  cart: {
    label: 'Cart Table',
    columns: ['ID', 'Order ID', 'Product SKU ID', 'Quantity', 'created_at'],
    fields: ['id', 'order_id', 'products_sku_id', 'quantity', 'created_at']
  }
};

// Left-side menu component: fixed vertical menu with two buttons
function LeftMenu({ showTable, setShowTable }) {
  const navigate = useNavigate();

  return (
    <nav className="left-menu" aria-label="Primary">
      <button
        className="menu-small"
        onClick={() => setShowTable(prev => !prev)}
        aria-pressed={showTable}
        title="Table List"
      >
        <TableIcon className="menu-icon" width={28} height={28} aria-hidden />
      </button>
      <div className="menu-label">Tables</div>

      <button
        className="menu-small"
        onClick={() => navigate('/')}
        title="Back to Home"
      >
        <HomeIcon className="menu-icon" width={22} height={22} aria-hidden />
      </button>
      <div className="menu-label">Home</div>
    </nav>
  );
}

function HomePage() {
  const [message, setMessage] = useState('');
  const [showArrow, setShowArrow] = useState(false);
  const [dataCount, setDataCount] = useState(1);
  const [loading, setLoading] = useState(false);
  const [genTime, setGenTime] = useState(null);
  const [commitTime, setCommitTime] = useState(null);
  const navigate = useNavigate();

  // Use custom typewriter hook
  const displayedText = useTypewriterEffect(message);

  // Handler for generating data
  const handleClick = useCallback(async () => {
    setShowArrow(false);
    setLoading(true);
    setMessage("");
    setGenTime(null);
    setCommitTime(null);
    try {
      const response = await fetch(API_ENDPOINTS.WRITE_TO_DB, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dataCount })
      });
      const data = await response.json();
      setMessage(data.message);
      if (typeof data.generation_time === 'number') setGenTime(data.generation_time);
      if (typeof data.commit_time === 'number') setCommitTime(data.commit_time);
      if (data.success === true) {
        setShowArrow(true);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage('Error fetching message.');
      setShowArrow(false);
    }
    setLoading(false);
  }, [dataCount]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>My e-commerce Page</h1>
        <div className="input-row">
          <label htmlFor="data-count" className="input-label">Rows to generate:</label>
          <input
            id="data-count"
            type="number"
            min={DATA_COUNT_LIMITS.MIN}
            max={DATA_COUNT_LIMITS.MAX}
            value={dataCount}
            onChange={e => setDataCount(validateDataCount(e.target.value))}
            className="input-style"
          />
          <button onClick={handleClick} disabled={loading}>
            {loading ? 'Generating...' : 'generate data'}
          </button>
        </div>
        {/* Show gen/commit time below input after generation completes */}
        {!loading && genTime !== null && commitTime !== null && (
          <div className="gen-commit-time">
            <div className="gen-commit-time-row">
              <span className="gen-commit-time-text">Gen: {genTime.toFixed(2)}s</span>
              <span className="gen-commit-time-text">Commit: {commitTime.toFixed(2)}s</span>
            </div>
          </div>
        )}
        {displayedText && <p className="typewriter-text">{displayedText}</p>}
        {showArrow && (
          <div className="arrow-container" onClick={() => navigate('/user-table')}>
            <span>View Data Table →</span>
          </div>
        )}
      </header>
    </div>
  );
}

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

        {/* Blinking down arrow removed from outside table, now only shown with table */}

        {/* Empty page below table-container */}
  <div ref={emptyPageRef} className="empty-page empty-page-style"></div>
        {/* Back-to-home button moved into left menu; removed duplicate button here. */}
      </header>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/user-table" element={<DataTablePage />} />
      </Routes>
    </Router>
  );
}

export default App;