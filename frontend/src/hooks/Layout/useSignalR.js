import { useEffect, useRef } from 'react';
import { HubConnectionBuilder } from '@microsoft/signalr';
import useAuthStore from '../../stores/authStore';

export function useSignalR(addNotification) {
  const connectionRef = useRef(null);
  const connectingRef = useRef(false);
  const { isLoggedIn } = useAuthStore();

  // Stop connection on logout
  useEffect(() => {
    if (!isLoggedIn && connectionRef.current) {
      console.log('SignalR: Stopping connection on logout');
      connectionRef.current.off('JobStatusUpdate');
      connectionRef.current.stop();
      connectionRef.current = null;
      connectingRef.current = false;
    }
  }, [isLoggedIn]);

  useEffect(() => {
    if (connectionRef.current || connectingRef.current || !isLoggedIn) return;

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

        // Use ref to always get the latest addNotification function
        const handler = (data) => {
          const jobData = Array.isArray(data) ? data[0] : data;
          addNotification('job', {
            id: jobData.id,
            message: jobData.message,
            status: jobData.status,
            timestamp: new Date().toISOString(),
          });
        };

        connection.on('JobStatusUpdate', handler);

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
        connectionRef.current.off('JobStatusUpdate');
        connectionRef.current.stop();
        connectionRef.current = null;
      }
      connectingRef.current = false;
    };
  }, [isLoggedIn]);
}