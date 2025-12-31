import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import useAuthStore from '../stores/authStore';

const PrivateRoute = () => {
  const isLoggedIn = useAuthStore((state) => state.isLoggedIn);

  return isLoggedIn ? <Outlet /> : <Navigate to="/" />;
};

export default PrivateRoute;
