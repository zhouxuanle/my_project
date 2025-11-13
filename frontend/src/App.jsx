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
  const navigate = useNavigate();

  const handleClick = useCallback(async () => {
    setShowArrow(false); // Hide arrow when starting new request
    
    try {
      const response = await fetch('http://127.0.0.1:5000/write_to_db',{
        method: 'POST'
      }); // Flask default port
      const data = await response.json();
      setMessage(data.message);
      
      // Show arrow only if no error occurred
      if (data.success === true) {
        setShowArrow(true);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage('Error fetching message.');
      setShowArrow(false);
    }
  }, []);


  useEffect(() => {
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

  return (
    <div className="App">
      <header className="App-header">
        <h1>My e-commerce Page</h1>
        <button onClick={handleClick}>generate data</button>
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
        <h1>Data Table</h1>

        {/* Left fixed menu (contains Back to Home and Table List) */}
        <LeftMenu showTable={showTable} setShowTable={setShowTable} />


        <div className="table-container">
          {/* All Table Buttons - Center */}
          {!showTable && (
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

          {/* Data Table - Hidden by default */}
          {showTable && (
            loading ? (
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
            )
          )}
        </div>

        {/* Blinking down arrow below the table-container */}
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