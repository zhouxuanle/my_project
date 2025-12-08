import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_ENDPOINTS } from '../constants';
import Panel from './ui/Panel';
import Button from './ui/Button';

function DataFolders() {
  const [folders, setFolders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchFolders() {
      setLoading(true);
      setError('');
      try {
        const token = localStorage.getItem('token');
        const res = await fetch(API_ENDPOINTS.LIST_PARENT_JOBS, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();
        if (data.success) {
          setFolders(data.parentJobIds);
        } else {
          setError(data.message || 'Failed to fetch folders');
        }
      } catch (e) {
        setError('Network error');
      }
      setLoading(false);
    }
    fetchFolders();
  }, []);

  return (
    <Panel>
      <h2 className="text-lg font-semibold mb-4">Your Data Folders</h2>
      {loading && <div>Loading...</div>}
      {error && <div className="text-red-500">{error}</div>}
      {!loading && !error && folders.length === 0 && <div>No folders found.</div>}
      <ul className="space-y-2">
        {folders.map((folder) => (
          <li key={folder}>
            <Button
              variant="primary"
              onClick={() => navigate(`/data/${folder}`)}
            >
              {folder}
            </Button>
          </li>
        ))}
      </ul>
    </Panel>
  );
}

export default DataFolders;
