// Use Vite environment variable. In the browser `process` is undefined,
// so use `import.meta.env.VITE_API_URL` which Vite replaces at build time.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';

const getHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
};

const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }));
    throw new Error(error.message || error.msg || `HTTP ${response.status}`);
  }
  return response;
};

export const api = {
  login: async (username, password) => {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    return handleResponse(response);
  },
  
  register: async (username, password) => {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    return handleResponse(response);
  },

  writeToDb: async (dataCount) => {
    const response = await fetch(`${API_BASE_URL}/write_to_db`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ dataCount }),
    });
    return handleResponse(response);
  },

  getTableData: async (tableName) => {
    const response = await fetch(`${API_BASE_URL}/get_${tableName}`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  generateRawData: async (dataCount) => {
    const response = await fetch(`${API_BASE_URL}/generate_raw`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ dataCount }),
    });
    return handleResponse(response);
  },

  getRawData: async (parentJobId, tableName) => {
    const response = await fetch(`${API_BASE_URL}/get_raw_data/${parentJobId}/${tableName}`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  listParentJobs: async () => {
    const response = await fetch(`${API_BASE_URL}/list_parent_jobs`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  }
};
