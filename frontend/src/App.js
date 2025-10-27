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

  useEffect(() => console.log(displayedText), [displayedText]);

  useEffect(() => {
    if (message) {
      setDisplayedText('');
      let index = 0;
      const timer = setInterval(() => {
        if (index < message.length) {
          let message_letter = message[index]
          console.log(message_letter,'----------');
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
          <div className="arrow-container" onClick={() => navigate('/data-table')}>
            <span>View Data Table</span>
            <div className="arrow-icon">→</div>
          </div>
        )}
      </header>
    </div>
  );
}

function DataTablePage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showTable, setShowTable] = useState(true);
  const [activeTable, setActiveTable] = useState('user'); // Track which table is active

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_users');
      const data = await response.json();
      if (data.success) {
        setUsers(data.users);
      }
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTableSelect = (tableName) => {
    setActiveTable(tableName);
    setShowTable(true);
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
      <header className="App-header data-table-header">
        <h1>Data Table</h1>
        <div className="table-container">
          {/* Table List Button - Top Left */}
          {showTable && (
            <button 
              className="table-list-button"
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
                  className="user-table-button"
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
            ) : users.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Real Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Sex</th>
                    <th>Age</th>
                    <th>Job</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user, index) => (
                    <tr key={index}>
                      <td>{user.id}</td>
                      <td>{user.user_name}</td>
                      <td>{user.real_name}</td>
                      <td>{user.email}</td>
                      <td>{user.phone_number}</td>
                      <td>{user.sex}</td>
                      <td>{user.age}</td>
                      <td>{user.job}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No users found.</p>
            )
          )}
          <button onClick={() => window.history.back()}>← Back to Home</button>
        </div>
      </header>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/data-table" element={<DataTablePage />} />
      </Routes>
    </Router>
  );
}

export default App;