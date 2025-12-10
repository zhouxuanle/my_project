import React from 'react';
import { useTypewriterEffect } from '../hooks';
import { DATA_COUNT_LIMITS } from '../constants';
import Button from './ui/Button';
import InputGroup from './ui/InputGroup';
import Panel from './ui/Panel';
import PageTitle from './ui/PageTitle';

function DataGenerationPanel({ dataCount, setDataCount, handleClick, generating, message, authMessage }) {
  const displayedText = useTypewriterEffect(message);

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