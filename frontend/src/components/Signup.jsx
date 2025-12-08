import React, { useState } from 'react';
import Button from './ui/Button';
import { api } from '../services/api';

function Signup({ onSuccess, switchToLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await api.register(username, password);
      
      const data = await response.json();
      
      if (response.ok) {
        // Auto login or just switch to login? Let's switch to login for now or auto-login if backend supported it.
        // For simplicity, let's just tell user to login.
        switchToLogin();
      } else {
        setError(data.msg || 'Signup failed');
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
      <form onSubmit={handleSignup} className="flex flex-col gap-4">
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
        <Button type="submit" variant="primary" disabled={loading}>
          {loading ? 'Signing up...' : 'Sign Up'}
        </Button>
      </form>
      <p className="text-sm text-gray-400 mt-2">
        Already have an account? <button onClick={switchToLogin} className="text-blue-400 hover:underline">Login</button>
      </p>
    </div>
  );
}

export default Signup;
