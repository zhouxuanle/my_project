import React, { useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTypewriterEffect } from '../hooks';
import { API_ENDPOINTS, DATA_COUNT_LIMITS } from '../constants';
import { validateDataCount } from '../utils';
import Button from './ui/Button';
import InputGroup from './ui/InputGroup';
import Panel from './ui/Panel';
import PageTitle from './ui/PageTitle';
import Modal from './ui/Modal';
import Login from './Login';
import Signup from './Signup';

function HomePage() {
  const [message, setMessage] = useState('');
  // Controls visibility of 'View Data Table' button
  const [showArrow, setShowArrow] = useState(() => {
    // Show only if not first visit
    return localStorage.getItem('hasViewedDataTable') === 'true';
  });
  const [dataCount, setDataCount] = useState(1);
  const [loading, setLoading] = useState(false);
  const [genTime, setGenTime] = useState(null);
  const [commitTime, setCommitTime] = useState(null);
  const [parentJobId, setParentJobId] = useState(null);
  
  // Auth State
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'signup'
  const [authMessage, setAuthMessage] = useState(''); // Message to show when unauthenticated user clicks generate

  const navigate = useNavigate();

  // Check login status on mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
    // If coming from user-table, show the button
    if (localStorage.getItem('hasViewedDataTable') === 'true') {
      setShowArrow(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    setIsLoggedIn(false);
    setShowArrow(false);
    setMessage('');
  };

  const openAuthModal = (mode = 'login') => {
    setAuthMode(mode);
    setShowAuthModal(true);
    setAuthMessage('');
  };

  const handleAuthSuccess = () => {
    setIsLoggedIn(true);
    setShowAuthModal(false);
    setAuthMessage('');
  };

  // Use custom typewriter hook
  const displayedText = useTypewriterEffect(message);

  // Handler for generating data
  const handleClick = useCallback(async () => {
    if (!isLoggedIn) {
      setAuthMessage('Please sign up or login to generate data.');
      return;
    }

    setShowArrow(false);
    setLoading(true);
    setMessage("");
    setGenTime(null);
    setCommitTime(null);
    setParentJobId(null);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(API_ENDPOINTS.GENERATE_RAW, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ dataCount })
      });
      const data = await response.json();
      setMessage(`Job submitted! ParentJob ID: ${data.parentJobId}, Status: ${data.status}`);
      if (data.parentJobId) {
        setParentJobId(data.parentJobId);
        setShowArrow(true);
        // Mark that user has viewed data table
        localStorage.setItem('hasViewedDataTable', 'true');
      }
    } catch (error) {
      console.error('Error submitting job:', error);
      setMessage('Error submitting job.');
      setShowArrow(false);
    }
    setLoading(false);
  }, [dataCount, isLoggedIn]);

  return (
    <div className="App relative">
      {/* Top Right Auth Buttons */}
      <div className="absolute top-4 right-4 flex gap-4 z-10">
        {isLoggedIn ? (
          <Button onClick={handleLogout}>Logout</Button>
        ) : (
          <>
            <Button onClick={() => openAuthModal('login')}>Login</Button>
            <Button onClick={() => openAuthModal('signup')}>Sign Up</Button>
          </>
        )}
      </div>

      <header className="App-header">
        <PageTitle>My e-commerce Page</PageTitle>
        
        <Panel>
          <InputGroup
            label="Rows to generate:"
            id="data-count"
            type="number"
            min={DATA_COUNT_LIMITS.MIN}
            max={DATA_COUNT_LIMITS.MAX}
            value={dataCount}
            onChange={e => setDataCount(validateDataCount(e.target.value))}
          />
          <div className="flex flex-col items-center gap-2">
            <Button onClick={handleClick} disabled={loading} variant="action">
              {loading ? 'Generating...' : 'Generate Data'}
            </Button>
            {authMessage && <p className="text-red-400 text-sm animate-pulse">{authMessage}</p>}
          </div>
        </Panel>
        {/* Show gen/commit time below input after generation completes */}
        {!loading && genTime !== null && commitTime !== null && (
            <div className="gen-commit-time-row">
              <span className="gen-commit-time-text">Gen: {genTime.toFixed(2)}s</span>
              <span className="gen-commit-time-text">Commit: {commitTime.toFixed(2)}s</span>
            </div>
        )}
        {!loading && displayedText && <p className="typewriter-text">{displayedText}</p>}
        {showArrow && (
          <Button variant="primary" onClick={() => navigate('/user-table', { state: { parentJobId: parentJobId } })}>
            <span>View Data Table →</span>
          </Button>
        )}
      </header>

      {/* Auth Modal */}
      <Modal 
        isOpen={showAuthModal} 
        onClose={() => setShowAuthModal(false)}
        title={authMode === 'login' ? 'Login' : 'Sign Up'}
      >
        {authMode === 'login' ? (
          <Login onSuccess={handleAuthSuccess} switchToSignup={() => setAuthMode('signup')} />
        ) : (
          <Signup onSuccess={handleAuthSuccess} switchToLogin={() => setAuthMode('login')} />
        )}
      </Modal>
    </div>
  );
}

export default HomePage;