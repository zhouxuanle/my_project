import React, { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { api } from '../services/api';
import useAuthStore from '../stores/authStore';

const PrivateRoute = () => {
  const isLoggedIn = useAuthStore((state) => state.isLoggedIn);
  const [checking, setChecking] = useState(false); // No initial checking

  /*
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
          try { localStorage.removeItem('token'); localStorage.removeItem('refresh_token'); } catch (_) {}
          if (mounted) setAuthed(false);
        }
      } else if (!token) {
        if (mounted) setAuthed(false);
      }
      // No need to set checking here
    };

    // Only run async check if we assumed auth from tokens
    if (authed) {
      check();
    }

    return () => { mounted = false; };
  }, [authed]); // Depend on authed to re-run if needed
  */

  return isLoggedIn ? <Outlet /> : <Navigate to="/" />;
};

export default PrivateRoute;
