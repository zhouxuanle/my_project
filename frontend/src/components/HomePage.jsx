import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useDataGeneration } from '../hooks/useDataGeneration';
import { useDataFolders, useSessionStorage } from '../hooks';
import AuthSection from './AuthSection';
import DataGenerationPanel from './DataGenerationPanel';
import ViewTableButton from './ViewTableButton';

function HomePage() {
  const [hasViewedTable, setHasViewedTable, removeHasViewedTable] = useSessionStorage('hasViewedTable', false);
  const [showViewTableButton, setShowViewTableButton] = useState(false);

  const { refresh: refreshFolders, hasFolder } = useDataFolders({ autoFetch: false });
  
  const auth = useAuth(refreshFolders);
  const dataGen = useDataGeneration(auth.isLoggedIn, auth.setAuthMessage, refreshFolders);

  // Keep showArrow derived from login status, whether user viewed table this session, or if folders exist
  useEffect(() => {
    if (auth.isLoggedIn && (hasViewedTable || hasFolder)) {
      setShowViewTableButton(true);
    } else {
      setShowViewTableButton(false);
    }
  }, [auth.isLoggedIn, hasViewedTable, hasFolder]);

  // On any refresh/hasFolder change: if there are no folders, clear the session flag
  // so a preserved `hasViewedTable` does not incorrectly keep the button visible.
  useEffect(() => {
    if (!hasFolder) {
      // Clear session flag when folders are gone so the button won't persist
      try {
        removeHasViewedTable();
      } catch (e) {
        console.warn('Failed clearing hasViewedTable from sessionStorage', e);
        setHasViewedTable(false);
      }
    }
  }, [hasFolder, removeHasViewedTable, setHasViewedTable]);

  return (
    <div className="App relative">
      <AuthSection
        isLoggedIn={auth.isLoggedIn}
        handleLogout={auth.handleLogout}
        showAuthModal={auth.showAuthModal}
        authMode={auth.authMode}
        openAuthModal={auth.openAuthModal}
        handleAuthSuccess={auth.handleAuthSuccess}
      />

      <header className="App-header">
        <DataGenerationPanel
          dataCount={dataGen.dataCount}
          setDataCount={dataGen.setDataCount}
          handleClick={dataGen.handleClick}
          generating={dataGen.generating}
          message={dataGen.message}
          authMessage={auth.authMessage}
        />

        <ViewTableButton
          showViewTableButton={showViewTableButton}
          parentJobId={dataGen.parentJobId}
          setHasViewedTable={setHasViewedTable}
        />
      </header>
    </div>
  );
}

export default HomePage;