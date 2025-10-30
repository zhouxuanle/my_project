import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css'; // For basic styling

function HomePage() {
  const [message, setMessage] = useState('');
  const [displayedText, setDisplayedText] = useState('');
  const [showArrow, setShowArrow] = useState(false);
  const navigate = useNavigate();

  const handleClick = async () => {
    setShowArrow(false); // Hide arrow when starting new request
    
    try {
      const response = await fetch('http://127.0.0.1:5000/write_to_db',{
        method: 'POST'
      }); // Flask default port
      const data = await response.json();
      setMessage(data.message);
      
      // Show arrow only if no error occurred
      if (data.success == true) {
        setShowArrow(true);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage('Error fetching message.');
      setShowArrow(false);
    }
  };


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

  useEffect(() => {
    fetchTableData(activeTable);
  }, [activeTable]);

// Generic fetch function
  const fetchTableData = async (tableName) => {
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
  };

  const handleTableSelect = (tableName) => {
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
  };

  const tables = [
    { name: 'user', label: 'User Table' },
    { name: 'address', label: 'Address Table' },
    { name: 'category', label: 'Category Table' },
    { name: 'subcategory', label: 'Subcategory Table' },
    { name: 'product', label: 'Product Table' },
    { name: 'products_sku', label: 'Products SKU Table' },
    { name: 'wishlist', label: 'Wishlist Table' },
    { name: 'payment', label: 'Payment Table' },
    { name: 'order', label: 'Order Table' },
    { name: 'order_item', label: 'Order Item Table' },
    { name: 'cart', label: 'Cart Table' }
  ];

  return (
    <div className="App">
      <header className="App-header">
        <h1>Data Table</h1>
        <div className="table-container">
          {/* Table List Button - Top Left */}
          {showTable && (
            <button 
              onClick={() => setShowTable(false)}
            >
              Table List
            </button>
          )}

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
                    {activeTable === 'user' && (
                      <>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Real Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Sex</th>
                        <th>Age</th>
                        <th>Job</th>
                      </>
                    )}
                    {activeTable === 'address' && (
                      <>
                        <th>ID</th>
                        <th>User ID</th>
                        <th>Title</th>
                        <th>Address Line</th>
                        <th>Country</th>
                        <th>City</th>
                        <th>Postal Code</th>
                      </>
                    )}
                    {activeTable === 'category' && (
                      <>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Description</th>
                      </>
                    )}
                    {activeTable === 'subcategory' && (
                      <>
                        <th>ID</th>
                        <th>Parent ID</th>
                        <th>Name</th>
                        <th>Description</th>
                      </>
                    )}
                    {activeTable === 'product' && (
                      <>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Category ID</th>
                      </>
                    )}
                    {activeTable === 'products_sku' && (
                      <>
                        <th>ID</th>
                        <th>Product ID</th>
                        <th>Price</th>
                        <th>Stock</th>
                      </>
                    )}
                    {activeTable === 'wishlist' && (
                      <>
                        <th>ID</th>
                        <th>User ID</th>
                        <th>Product SKU ID</th>
                      </>
                    )}
                    {activeTable === 'payment' && (
                      <>
                        <th>ID</th>
                        <th>Amount</th>
                        <th>Provider</th>
                        <th>Status</th>
                      </>
                    )}
                    {activeTable === 'order' && (
                      <>
                        <th>ID</th>
                        <th>User ID</th>
                        <th>Payment ID</th>
                      </>
                    )}
                    {activeTable === 'order_item' && (
                      <>
                        <th>ID</th>
                        <th>Order ID</th>
                        <th>Product SKU ID</th>
                        <th>Quantity</th>
                      </>
                    )}
                    {activeTable === 'cart' && (
                      <>
                        <th>ID</th>
                        <th>Order ID</th>
                        <th>Product SKU ID</th>
                        <th>Quantity</th>
                      </>
                    )}
                  </tr>
                </thead>
                <tbody>
                  {tableData.map((data, index) => (
                    <tr key={index}>
                      {activeTable === 'user' && (
                        <>
                          <td>{data.id}</td>
                          <td>{data.user_name}</td>
                          <td>{data.real_name}</td>
                          <td>{data.email}</td>
                          <td>{data.phone_number}</td>
                          <td>{data.sex}</td>
                          <td>{data.age}</td>
                          <td>{data.job}</td>
                        </>
                      )}
                      {activeTable === 'address' && (
                        <>
                          <td>{data.id}</td>
                          <td>{data.user_id}</td>
                          <td>{data.title}</td>
                          <td>{data.address_line}</td>
                          <td>{data.country}</td>
                          <td>{data.city}</td>
                          <td>{data.postal_code}</td>
                        </>
                      )}
                      {activeTable === 'category' && (
                        <>
                          <td>{data.id}</td>
                          <td>{data.name}</td>
                          <td>{data.description}</td>
                        </>
                      )}
                      {activeTable === 'subcategory' && (
                        <>
                          <td>{data.id}</td>
                          <td>{data.parent_id}</td>
                          <td>{data.name}</td>
                          <td>{data.description}</td>
                        </>
                      )}
                      {activeTable === 'product' && (
                        <>
                          <td>{data.id}</td>
                          <td>{data.name}</td>
                          <td>{data.description}</td>
                          <td>{data.category_id}</td>
                        </>
                      )}
                      {activeTable === 'products_sku' && (
                        <>
                          <td>{data.id}</td>
                          <td>{data.product_id}</td>
                          <td>{data.price}</td>
                          <td>{data.quantity}</td>
                        </>
                      )}
                      {activeTable === 'wishlist' && (
                        <>
                          <td>{data.id}</td>
                          <td>{data.user_id}</td>
                          <td>{data.products_sku_id}</td>
                        </>
                      )}
                      {activeTable === 'payment' && (
                        <>
                          <td>{data.id}</td>
                          <td>{data.amount}</td>
                          <td>{data.provider}</td>
                          <td>{data.status}</td>
                        </>
                      )}
                      {activeTable === 'order' && (
                        <>
                          <td>{data.id}</td>
                          <td>{data.user_id}</td>
                          <td>{data.payment_id}</td>
                        </>
                      )}
                      {activeTable === 'order_item' && (
                        <>
                          <td>{data.id}</td>
                          <td>{data.order_id}</td>
                          <td>{data.products_sku_id}</td>
                          <td>{data.quantity}</td>
                        </>
                      )}
                      {activeTable === 'cart' && (
                        <>
                          <td>{data.id}</td>
                          <td>{data.order_id}</td>
                          <td>{data.products_sku_id}</td>
                          <td>{data.quantity}</td>
                        </>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No {activeTable} data found.</p>
            )
          )}
          
        </div>
        <button className="back-to-home-button" onClick={() => window.history.back()}>← Back to Home</button>
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