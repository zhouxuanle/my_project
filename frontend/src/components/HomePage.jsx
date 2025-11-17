import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTypewriterEffect } from '../hooks';
import { API_ENDPOINTS, DATA_COUNT_LIMITS } from '../constants';
import { validateDataCount } from '../utils';

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

export default HomePage;