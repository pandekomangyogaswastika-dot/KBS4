import axios from "axios";

// Demo API base — selalu ke /api/demo/kn3
export const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api/demo/kn3`;

// Set demo session token sebagai Authorization header
export const setAuthToken = (token) => {
  if (token) axios.defaults.headers.common.Authorization = `Bearer ${token}`;
  else delete axios.defaults.headers.common.Authorization;
};

export default axios;
