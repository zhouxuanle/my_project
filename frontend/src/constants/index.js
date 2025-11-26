// API endpoint constants
const API_BASE_URL = 'http://127.0.0.1:5000';

export const API_ENDPOINTS = {
  WRITE_TO_DB: `${API_BASE_URL}/write_to_db`,
  GENERATE_RAW: `${API_BASE_URL}/generate_raw`,
  GET_TABLE: (tableName) => `${API_BASE_URL}/get_${tableName}`,
  GET_RAW_DATA: (jobId, tableName) => `${API_BASE_URL}/get_raw_data/${jobId}/${tableName}`
};

// Input validation constants
export const DATA_COUNT_LIMITS = {
  MIN: 1,
  MAX: 999999
};

// Responsive breakpoint constants
export const BREAKPOINTS = {
  SMALL: 600,
  MEDIUM: 700,
  LARGE: 900
};