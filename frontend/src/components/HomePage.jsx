import React, { useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTypewriterEffect, useDataFolders, useGenerateJob, useSessionStorage } from '../hooks';
import { DATA_COUNT_LIMITS } from '../constants';
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
  // Controls visibility of the 'View Data Table' button
  const [showViewTableButton, setShowViewTableButton] = useState(false);
  // Tracks if the button has ever been shown in this session (persisted in sessionStorage)
  const [hasViewedTable, setHasViewedTable, removeHasViewedTable] = useSessionStorage('hasViewedTable', false);
  const [dataCount, setDataCount] = useState(1);
  const [parentJobId, setParentJobId] = useState(null);
  
  // Auth State
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'signup'
  const [authMessage, setAuthMessage] = useState(''); // Message to show when unauthenticated user clicks generate

  const navigate = useNavigate();

  const { refresh: refreshFolders, hasFolder } = useDataFolders({ autoFetch: false });
  const { generate, loading: generating } = useGenerateJob();

  // Check login status on mount and fetch folders if logged in
  useEffect(() => {
    const token = localStorage.getItem('token');
    const loggedIn = !!token;
    setIsLoggedIn(loggedIn);
    if (loggedIn) refreshFolders();
  }, [refreshFolders]);

  // Keep showArrow derived from login status, whether user viewed table this session, or if folders exist
  useEffect(() => {
    if (isLoggedIn && (hasViewedTable || hasFolder)) {
      setShowViewTableButton(true);
    } else {
      setShowViewTableButton(false);
    }
  }, [isLoggedIn, hasViewedTable, hasFolder]);

  // On any refresh/hasFolder change: if there are no folders, clear the session flag
  // so a preserved `hasViewedTable` does not incorrectly keep the button visible.
  useEffect(() => {
    if (!hasFolder) {
      // Clear session flag when folders are gone so the button won't persist
      try {
        removeHasViewedTable();
      } catch (e) {
        // eslint-disable-next-line no-console
        console.warn('Failed clearing hasViewedTable from sessionStorage', e);
        setHasViewedTable(false);
      }
    }
  }, [hasFolder, removeHasViewedTable, setHasViewedTable]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    setIsLoggedIn(false);
    setShowViewTableButton(false);
    setHasViewedTable(false);
    try {
      removeHasViewedTable();
    } catch (e) {
      // eslint-disable-next-line no-console
      console.warn('Failed removing session flag on logout', e);
    }
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
    // After successful login, refresh folder info
    refreshFolders();
  };

  // Use custom typewriter hook
  const displayedText = useTypewriterEffect(message);

  // Handler for generating data
  const handleClick = useCallback(async () => {
    if (!isLoggedIn) {
      setAuthMessage('Please sign up or login to generate data.');
      return;
    }

    setShowViewTableButton(false);
    setMessage("");
    setParentJobId(null);
    
    try {
      const data = await generate(dataCount);
      setMessage(`Job submitted! ParentJob ID: ${data.parentJobId}, Status: ${data.status}`);
      if (data.parentJobId) {
        setParentJobId(data.parentJobId);
        setShowViewTableButton(true);
        refreshFolders(); // Refresh folder list after successful generation
      }
    } catch (error) {
      console.error('Error submitting job:', error);
      setMessage('Error submitting job.');
      setShowViewTableButton(false);
    }
  }, [dataCount, isLoggedIn, generate, refreshFolders]);

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
            <Button onClick={handleClick} disabled={generating} variant="action">
              {generating ? 'Generating...' : 'Generate Data'}
            </Button>
            {authMessage && <p className="text-red-400 text-sm animate-pulse">{authMessage}</p>}
          </div>
        </Panel>
        {/* generation timing removed — not set anywhere (keeps UI clean) */}
        {!generating && displayedText && <p className="typewriter-text">{displayedText}</p>}
        {showViewTableButton && (
          <Button
            variant="primary"
            onClick={() => {
              setHasViewedTable(true);
              navigate('/user-table', { state: { parentJobId: parentJobId } });
            }}
          >
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