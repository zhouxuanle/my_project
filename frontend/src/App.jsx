import React, { useState, useEffect, useMemo, useCallback } from 'react';
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
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css'; // For basic styling

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
      {/* Table List button (now matches the Home button shape) */}
      <button
        className="menu-small"
        onClick={() => setShowTable(prev => !prev)}
        aria-pressed={showTable}
        title="Table List"
      >
        {/* Sheet/table SVG icon */}
        <svg className="menu-icon" width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
          <rect x="3" y="4" width="18" height="16" rx="2" stroke="white" strokeWidth="1.4" fill="none" />
          {/* horizontal header line */}
          <path d="M3 8.5h18" stroke="white" strokeWidth="1.4" strokeLinecap="round" />
          {/* vertical divider for columns */}
          <path d="M9.5 8.5v11" stroke="white" strokeWidth="1.4" strokeLinecap="round" />
          <path d="M15.5 8.5v11" stroke="white" strokeWidth="1.4" strokeLinecap="round" />
          {/* a couple of subtle row lines */}
          <path d="M3 13.5h18" stroke="white" strokeWidth="1" strokeLinecap="round" opacity="0.9" />
        </svg>
      </button>
  <div className="menu-label">Tables</div>

      {/* Smaller home button */}
      <button
        className="menu-small"
        onClick={() => navigate('/')}
        title="Back to Home"
      >
        <svg className="menu-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
          <path d="M3 10.5L12 4l9 6.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1V10.5z" fill="white" />
        </svg>
      </button>
      <div className="menu-label">Home</div>
    </nav>
  );
}

function HomePage() {
  const [message, setMessage] = useState('');
  const [displayedText, setDisplayedText] = useState('');
  const [showArrow, setShowArrow] = useState(false);
  const [dataCount, setDataCount] = useState(1);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const navigate = useNavigate();
  const [genTime, setGenTime] = useState(0);
  const [commitTime, setCommitTime] = useState(0);
  const [finalGenTime, setFinalGenTime] = useState(null);
  const [finalCommitTime, setFinalCommitTime] = useState(null);
  const [timingPhase, setTimingPhase] = useState('idle'); // 'idle' | 'generating' | 'committing' | 'done'
  const genTimerRef = React.useRef();
  const commitTimerRef = React.useRef();

  const handleClick = useCallback(async () => {
    setShowArrow(false);
    setLoading(true);
    setMessage("");
    setProgress(0);
    setGenTime(0);
    setCommitTime(0);
    setFinalGenTime(null);
    setFinalCommitTime(null);
    setTimingPhase('generating');
    // Start generation timer
    if (genTimerRef.current) clearInterval(genTimerRef.current);
    if (commitTimerRef.current) clearInterval(commitTimerRef.current);
    let genStart = Date.now();
    genTimerRef.current = setInterval(() => {
      setGenTime(((Date.now() - genStart) / 1000));
    }, 50);
    // Simulate progress bar
    const fakeProgress = async () => {
      for (let i = 1; i <= dataCount; i++) {
        setProgress(i);
        if (i === dataCount) {
          // Stop gen timer when progress reaches 100
          if (genTimerRef.current) clearInterval(genTimerRef.current);
          setTimingPhase('committing');
          // Start commit timer
          let commitStart = Date.now();
          commitTimerRef.current = setInterval(() => {
            setCommitTime(((Date.now() - commitStart) / 1000));
          }, 50);
        }
        await new Promise(res => setTimeout(res, Math.max(10, 1000 / dataCount)));
      }
    };
    fakeProgress();
    try {
      const response = await fetch('http://127.0.0.1:5000/write_to_db', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dataCount })
      });
      const data = await response.json();
      // Set final times from backend for accuracy
      setFinalGenTime(data.generation_time || genTime);
      setFinalCommitTime(data.commit_time || commitTime);
      setTimingPhase('done');
      // Stop commit timer
      if (commitTimerRef.current) clearInterval(commitTimerRef.current);
      setMessage(data.message);
      // When backend responds, immediately set genTime to backend's value for display
      setGenTime(data.generation_time || genTime);
      if (data.success === true) {
        setShowArrow(true);
      }
    } catch (error) {
      if (genTimerRef.current) clearInterval(genTimerRef.current);
      if (commitTimerRef.current) clearInterval(commitTimerRef.current);
      setTimingPhase('idle');
      console.error('Error fetching data:', error);
      setMessage('Error fetching message.');
      setShowArrow(false);
    }
    setLoading(false);
    setProgress(0);
  }, [dataCount]);


  React.useEffect(() => {
    if (message) {
      setDisplayedText('');
      let index = 0;
      const timer = setInterval(() => {
        if (index < message.length) {
          let message_letter = message[index]
          setDisplayedText(prev => prev + message_letter);
          index++;
        } else {
          clearInterval(timer);
        }
      }, 50); 
      
      return () => clearInterval(timer);
    }
  }, [message]);

  // Cleanup timers on unmount
  React.useEffect(() => {
    return () => {
      if (genTimerRef.current) clearInterval(genTimerRef.current);
      if (commitTimerRef.current) clearInterval(commitTimerRef.current);
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>My e-commerce Page</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', justifyContent: 'center', marginBottom: '1rem' }}>
          <label htmlFor="data-count" style={{ fontWeight: 500 }}>Rows to generate:</label>
          <input
            id="data-count"
            type="number"
            min={1}
            max={999999}
            value={dataCount}
            onChange={e => setDataCount(Math.max(1, Math.min(999999, Number(e.target.value))))}
            style={{ width: '250px', padding: '0.3rem', borderRadius: '6px', border: '1px solid #ccc', textAlign: 'center', color: 'black' }}
          />
          <button onClick={handleClick} disabled={loading}>
            {loading ? 'Generating...' : 'generate data'}
          </button>
        </div>
        {loading && (
          <div style={{ width: '100%', maxWidth: 600, margin: '0 auto 1rem auto', padding: '0 1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <div style={{ flex: 1, background: '#eee', borderRadius: 8, height: 18, overflow: 'hidden' }}>
                <div style={{ width: `${Math.round((progress / dataCount) * 100)}%`, background: '#7c3aed', height: '100%', transition: 'width 0.2s', borderRadius: 8 }} />
              </div>
              <span style={{ minWidth: 80, fontWeight: 500, color: '#fff', fontSize: 14 }}>{progress} / {dataCount}</span>
            </div>
          </div>
        )}
        {!loading && finalGenTime !== null && finalCommitTime !== null && (
          <div style={{ width: '100%', maxWidth: 600, margin: '0 auto 1rem auto', padding: '0 1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, justifyContent: 'center' }}>
              <span style={{ minWidth: 120, fontWeight: 500, color: '#fff', fontSize: 14 }}>
                Gen: {finalGenTime.toFixed(2)}s
              </span>
              <span style={{ minWidth: 120, fontWeight: 500, color: '#fff', fontSize: 14 }}>
                Commit: {finalCommitTime.toFixed(2)}s
              </span>
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
  // You can adjust these breakpoints and min columns as needed
  let maxColumns = currentTableConfig.columns.length;
  if (windowWidth < 600) {
    maxColumns = Math.max(2, maxColumns - 6); // show only 2 columns on very small screens
  } else if (windowWidth < 700) {
    maxColumns = Math.max(3, maxColumns - 4); // show 3 columns
  } else if (windowWidth < 900) {
    maxColumns = Math.max(4, maxColumns - 3); // show 4 columns
  } // else show all columns

  // Always keep 'created_at' as the rightmost column if it exists
  const colIdx = currentTableConfig.fields.indexOf('created_at');

  let visibleColumns, visibleFields;
  if (colIdx !== -1) {
    // Remove 'created_at' from the list if present
    const columnsWithoutCreatedAt = currentTableConfig.columns.filter((_, idx) => idx !== colIdx);
    const fieldsWithoutCreatedAt = currentTableConfig.fields.filter((f) => f !== 'created_at');
    // Show up to maxColumns-1 columns, then add 'created_at' at the end
    const slicedColumns = columnsWithoutCreatedAt.slice(0, Math.max(1, maxColumns - 1));
    const slicedFields = fieldsWithoutCreatedAt.slice(0, Math.max(1, maxColumns - 1));
    visibleColumns = [...slicedColumns, currentTableConfig.columns[colIdx]];
    visibleFields = [...slicedFields, 'created_at'];
  } else {
    visibleColumns = currentTableConfig.columns.slice(0, maxColumns);
    visibleFields = currentTableConfig.fields.slice(0, maxColumns);
  }

  // Generic fetch function with useCallback for optimization
  const fetchTableData = useCallback(async (tableName) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/get_${tableName}`);
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

  useEffect(() => {
    fetchTableData(activeTable);
  }, [activeTable]);

  const handleTableSelect = useCallback((tableName) => {
    // Clear the current table data and show loading state immediately
    setTableData([]);
    setLoading(true);
    setShowTable(true);

    // If the user clicked the already-active table, activeTable won't change
    // so useEffect won't re-run — manually refetch in that case.
    if (tableName === activeTable) {
      fetchTableData(tableName);
    }

    // Otherwise update activeTable; the useEffect will trigger a fetch
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
  const emptyPageRef = React.useRef(null);

  // Handler to scroll to empty page
  const handleArrowClick = () => {
    if (emptyPageRef.current) {
      emptyPageRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

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
                      <tr key={index}>
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
              className="blinking-arrow"
              onClick={handleArrowClick}
              aria-label="Scroll to next section"
              style={{ background: 'none', border: 'none', cursor: 'pointer', outline: 'none' }}
            >
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ display: 'block' }}>
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </button>
          </div>
        )}

        {/* Blinking down arrow removed from outside table, now only shown with table */}

        {/* Empty page below table-container */}
        <div ref={emptyPageRef} className="empty-page" style={{ minHeight: '800px' }}></div>
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