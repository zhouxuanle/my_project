import React, { useState } from 'react';
import './App.css'; // For basic styling

function App() {
  const [message, setMessage] = useState('');

  const handleClick = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/hello'); // Flask default port
      const data = await response.json();
      setMessage(data.message);
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage('Error fetching message.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>My Awesome Page</h1>
        <button onClick={handleClick}>Say Hello</button>
        {message && <p>{message}</p>}
      </header>
    </div>
  );
}

export default App;