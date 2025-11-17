// API endpoint constants
const API_BASE_URL = 'http://127.0.0.1:5000';

export const API_ENDPOINTS = {
  WRITE_TO_DB: `${API_BASE_URL}/write_to_db`,
  GET_TABLE: (tableName) => `${API_BASE_URL}/get_${tableName}`
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