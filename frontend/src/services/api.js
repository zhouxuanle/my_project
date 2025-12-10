// Use Vite environment variable. In the browser `process` is undefined,
// so use `import.meta.env.VITE_API_URL` which Vite replaces at build time.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';

const getHeaders = (extraHeaders = {}) => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...extraHeaders
  };
};

const handleResponse = async (response) => {
  if (!response.ok) {
    const body = await response.json().catch(() => ({ message: 'Request failed' }));
    const err = new Error(body.message || body.msg || `HTTP ${response.status}`);
    err.status = response.status;
    err.body = body;
    throw err;
  }
  return response;
};

// Internal helper: perform fetch, attempt refresh on 401 and retry once
const fetchWithAuth = async (input, init = {}) => {
  init.headers = getHeaders(init.headers);
  let res = await fetch(input, init);
  if (res.status === 401) {
    // try refresh
    try {
      const refreshRes = await api.refresh();
      const refreshBody = await refreshRes.json();
      if (refreshBody.access_token) {
        localStorage.setItem('token', refreshBody.access_token);
        init.headers = getHeaders(init.headers);
        res = await fetch(input, init);
      }
    } catch (e) {
      // Refresh failed: clear stored tokens to avoid replaying invalid tokens
      try {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
      } catch (_) {}
      const err = new Error('Unauthorized - refresh failed');
      err.status = 401;
      throw err;
    }
  }
  return handleResponse(res);
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
    return fetchWithAuth(`${API_BASE_URL}/write_to_db`, {
      method: 'POST',
      body: JSON.stringify({ dataCount }),
    });
  },

  getTableData: async (tableName) => {
    return fetchWithAuth(`${API_BASE_URL}/get_${tableName}`, { method: 'GET' });
  },

  generateRawData: async (dataCount) => {
    return fetchWithAuth(`${API_BASE_URL}/generate_raw`, {
      method: 'POST',
      body: JSON.stringify({ dataCount }),
    });
  },

  getRawData: async (parentJobId, tableName) => {
    return fetchWithAuth(`${API_BASE_URL}/get_raw_data/${parentJobId}/${tableName}`, { method: 'GET' });
  },

  listParentJobs: async () => {
    return fetchWithAuth(`${API_BASE_URL}/list_parent_jobs`, { method: 'GET' });
  },

  // Refresh access token using refresh token
  refresh: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      const err = new Error('No refresh token available');
      err.status = 401;
      throw err;
    }
    const response = await fetch(`${API_BASE_URL}/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${refreshToken}`
      }
    });
    return handleResponse(response);
  }
};
