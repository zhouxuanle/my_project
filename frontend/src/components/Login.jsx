import React, { useState } from 'react';
import Button from './ui/Button';
import { api } from '../services/api';

function Login({ onSuccess, switchToSignup }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await api.login(username, password);
      
      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('token', data.access_token);
        // store refresh token for session continuation (dev use)
        if (data.refresh_token) {
          localStorage.setItem('refresh_token', data.refresh_token);
        }
        localStorage.setItem('userId', data.user_id);
        onSuccess();
      } else {
        setError(data.msg || 'Login failed');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      {error && <div className="bg-red-500/20 border border-red-500 text-red-200 p-3 rounded text-sm">{error}</div>}
      <form onSubmit={handleLogin} className="flex flex-col gap-4">
        <div className="flex flex-col gap-1 text-left">
          <label className="text-sm text-gray-300">Username</label>
          <input 
            type="text" 
            className="bg-gray-700 border border-gray-600 rounded p-2 text-white focus:border-blue-500 focus:outline-none"
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            required 
          />
        </div>
        <div className="flex flex-col gap-1 text-left">
          <label className="text-sm text-gray-300">Password</label>
          <input 
            type="password" 
            className="bg-gray-700 border border-gray-600 rounded p-2 text-white focus:border-blue-500 focus:outline-none"
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
        </div>
        <Button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </Button>
      </form>
      <p className="text-sm text-gray-400 mt-2">
        Don't have an account? <button onClick={switchToSignup} className="text-blue-400 hover:underline">Sign up</button>
      </p>
    </div>
  );
}

export default Login;
