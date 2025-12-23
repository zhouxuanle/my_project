import { useEffect, useRef } from 'react';
import { HubConnectionBuilder } from '@microsoft/signalr';

// Global flag to ensure the event handler is set only once
let handlerSet = false;

export function useSignalR(addNotification) {
  const connectionRef = useRef(null);
  const connectingRef = useRef(false);

  useEffect(() => {
    if (connectionRef.current || connectingRef.current) return;

    const connectSignalR = async () => {
      connectingRef.current = true;
      try {
        const response = await fetch('/api/negotiate');
        if (!response.ok) throw new Error(`Negotiate failed: ${response.status}`);
        const connectionInfo = await response.json();

        const connection = new HubConnectionBuilder()
          .withUrl(connectionInfo.url, {
            accessTokenFactory: () => connectionInfo.accessToken
          })
          .withAutomaticReconnect()
          .build();

        // Set the event handler only once globally
        if (!handlerSet) {
          connection.on('JobStatusUpdate', (data) => {
            const jobData = Array.isArray(data) ? data[0] : data;
            addNotification('job', {
              id: `${jobData.jobId}-${Date.now()}`,
              message: jobData.message || 'Job completed',
              timestamp: new Date().toISOString(),
            });
          });
          handlerSet = true;
        }

        await connection.start();
        connectionRef.current = connection;
      } catch (err) {
        console.error('SignalR: Connection failed', err);
      } finally {
        connectingRef.current = false;
      }
    };

    connectSignalR();

    return () => {
      if (connectionRef.current) {
        connectionRef.current.stop();
        connectionRef.current = null;
      }
    };
  }, []);
}