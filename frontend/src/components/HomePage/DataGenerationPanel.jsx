import React, { useEffect, useState } from 'react';
import { useTypewriterEffect, useLayout } from '../../hooks';
import { DATA_COUNT_LIMITS } from '../../constants';
import Button from '../ui/Button';
import InputGroup from '../ui/InputGroup';
import Panel from '../ui/Panel';
import PageTitle from '../ui/PageTitle';

function DataGenerationPanel({ dataCount, setDataCount, handleClick, generating, message, authMessage, refreshFolders }) {
  const { notifications } = useLayout();
  const [currentMessage, setCurrentMessage] = useState(message);

  // Update currentMessage when message prop changes (for submitted message)
  useEffect(() => {
    setCurrentMessage(message);
  }, [message]);

  useEffect(() => {
    // If notifications exist, overwrite with the latest notification (for completion)
    if (notifications.job.length > 0) {
      const latestJobNotification = notifications.job[0];
      setCurrentMessage(latestJobNotification.message);
      if (refreshFolders) refreshFolders(); // Refresh folders after completion
    }
  }, [notifications.job, refreshFolders]);

  const displayedText = useTypewriterEffect(currentMessage);

  return (
    <>
      <PageTitle>My e-commerce Page</PageTitle>
      <Panel>
        <InputGroup
          label="Rows to generate:"
          id="data-count"
          type="number"
          min={DATA_COUNT_LIMITS.MIN}
          max={DATA_COUNT_LIMITS.MAX}
          value={dataCount}
          onChange={e => setDataCount(e.target.value)}
        />
        <div className="flex flex-col items-center gap-2">
          <Button onClick={handleClick} disabled={generating} variant="action">
            {generating ? 'Generating...' : 'Generate Data'}
          </Button>
          {authMessage && <p className="text-red-400 text-sm animate-pulse">{authMessage}</p>}
        </div>
      </Panel>
      {!generating && displayedText && <p className="typewriter-text">{displayedText}</p>}
    </>
  );
}

export default DataGenerationPanel;