import { useCallback } from 'react';
import useGenerateJob from './useGenerateJob';
import useDataStore from '../stores/dataStore';
import { validateDataCount } from '../utils';

export function useDataGeneration(isLoggedIn, setAuthMessage, refreshFolders) {
  const {
    message,
    dataCount,
    parentJobId,
    generating,
    setMessage,
    setDataCountValue,
    setParentJobId,
    setGenerating,
  } = useDataStore();

  // useGenerateJob() is a hook , not function
  const { generate } = useGenerateJob();

  const handleClick = useCallback(async () => {
    if (!isLoggedIn) {
      setAuthMessage('Please sign up or login to generate data.');
      return;
    }

    setMessage("");
    setParentJobId(null);
    setGenerating(true);
    
    try {
      const data = await generate(dataCount);
      setMessage(`Job submitted! ParentJob ID: ${data.parentJobId}, Status: ${data.status}`);
      if (data.parentJobId) {
        setParentJobId(data.parentJobId);
      }
      if (refreshFolders) refreshFolders(); // Refresh folders after generation
    } catch (error) {
      console.error('Error submitting job:', error);
      setMessage('Error submitting job.');
    } finally {
      setGenerating(false);
    }
  }, [dataCount, isLoggedIn, generate, setAuthMessage, refreshFolders, setMessage, setParentJobId, setGenerating]);

  const handleSetDataCount = (value) => {
    setDataCountValue(validateDataCount(value));
  };

  return {
    message,
    dataCount,
    setDataCount: handleSetDataCount,
    parentJobId,
    generating,
    handleClick,
    setMessage,
  };
}
