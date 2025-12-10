import React, { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { api } from '../services/api';

const PrivateRoute = () => {
  const [checking, setChecking] = useState(true);
  const [authed, setAuthed] = useState(false);

  useEffect(() => {
    let mounted = true;

    const check = async () => {
      const token = localStorage.getItem('token');
      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          const res = await api.refresh();
          const body = await res.json();
          if (body.access_token) {
            localStorage.setItem('token', body.access_token);
            if (mounted) setAuthed(true);
          } else {
            if (mounted) setAuthed(false);
          }
        } catch (e) {
          // refresh failed -> clear tokens
          try { localStorage.removeItem('token'); localStorage.removeItem('refresh_token'); } catch (_) {}
          if (mounted) setAuthed(false);
        }
      } else if (token) {
        // No refresh token but access token exists — assume still valid for now
        if (mounted) setAuthed(true);
      } else {
        if (mounted) setAuthed(false);
      }

      if (mounted) setChecking(false);
    };

    check();

    return () => { mounted = false; };
  }, []);

  if (checking) return <div style={{ padding: 20 }}>Checking authentication...</div>;
  return authed ? <Outlet /> : <Navigate to="/" />;
};

export default PrivateRoute;
