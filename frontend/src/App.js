import React, { useState, useEffect } from 'react';
import './App.css'; // For basic styling

function App() {
  const [message, setMessage] = useState('');
  const [displayedText, setDisplayedText] = useState('');

  const handleClick = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/write_to_db',{
        method: 'POST'
      }); // Flask default port
      const data = await response.json();
      setMessage(data.message);
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage('Error fetching message.');
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
        <h1>My Awesome Page</h1>
        <button onClick={handleClick}>Say Hello</button>
        {displayedText && <p className="typewriter-text">{displayedText}</p>}
      </header>
    </div>
  );
}

export default App;