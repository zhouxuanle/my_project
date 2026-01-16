import { useEffect, useRef } from 'react';
import { HubConnectionBuilder } from '@microsoft/signalr';
import useAuthStore from '../../stores/authStore';
import { ConsoleLogger } from '@microsoft/signalr/dist/esm/Utils';

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
    console.log('SignalR: useEffect triggered');
    if (connectionRef.current || connectingRef.current || !isLoggedIn) return;

    const connectSignalR = async () => {
      connectingRef.current = true;
      try {
        const userId = localStorage.getItem('userId');
        if (!userId) {
          console.error('SignalR: No userId found in localStorage');
          return;
        }

        console.log('SignalR: Negotiating connection for userId:', userId);
        const response = await fetch(`/api/negotiate?userId=${encodeURIComponent(userId)}`);
        if (!response.ok) throw new Error(`Negotiate failed: ${response.status}`);
        const connectionInfo = await response.json();
        console.log('SignalR: Negotiate successful, building connection');

        const connection = new HubConnectionBuilder()
          .withUrl(connectionInfo.url, {
            accessTokenFactory: () => connectionInfo.accessToken
          })
          .withAutomaticReconnect()
          .build();

        // Use ref to always get the latest addNotification function
        const handler = (data) => {
          console.log('SignalR: JobStatusUpdate received:', data);
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
        console.log('SignalR: Connection started successfully');
        connectionRef.current = connection;
      } catch (err) {
        console.error('SignalR: Connection failed', err);
        // Clean up on connection failure
        if (connectionRef.current) {
          connectionRef.current.off('JobStatusUpdate');
          connectionRef.current.stop();
          connectionRef.current = null;
        }
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