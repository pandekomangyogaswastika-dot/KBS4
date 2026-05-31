import axios from "axios";
import { useCallback, useEffect, useRef, useState } from "react";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export const api = axios.create({ baseURL: API });

export function setTokens({ access, refresh }) {
  if (access) localStorage.setItem("kti_token", access);
  if (refresh) localStorage.setItem("kti_refresh", refresh);
}

export function clearTokens() {
  localStorage.removeItem("kti_token");
  localStorage.removeItem("kti_refresh");
}

export function apiError(err, fallback = "Terjadi kesalahan") {
  return err?.response?.data?.error?.message || err?.message || fallback;
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("kti_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

let refreshPromise = null;
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config || {};
    const status = error?.response?.status;
    const code = error?.response?.data?.error?.code;
    const url = original.url || "";
    if (status === 401 && code === "AUTH_TOKEN_EXPIRED" && !original._retry && !url.includes("/auth/")) {
      original._retry = true;
      const rt = localStorage.getItem("kti_refresh");
      if (!rt) {
        clearTokens();
        window.dispatchEvent(new Event("kti-auth-expired"));
        return Promise.reject(error);
      }
      try {
        if (!refreshPromise) {
          refreshPromise = axios
            .post(`${API}/auth/refresh`, { refresh_token: rt })
            .finally(() => { refreshPromise = null; });
        }
        const r = await refreshPromise;
        const newAccess = r.data?.data?.access_token;
        if (newAccess) {
          localStorage.setItem("kti_token", newAccess);
          original.headers = original.headers || {};
          original.headers.Authorization = `Bearer ${newAccess}`;
          return api(original);
        }
      } catch (e) {
        clearTokens();
        window.dispatchEvent(new Event("kti-auth-expired"));
      }
    }
    return Promise.reject(error);
  }
);

// Simple fetch hook for GET endpoints returning {success, data} (+ optional meta).
export function useFetch(path, deps = []) {
  const [data, setData] = useState(null);
  const [meta, setMeta] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const mounted = useRef(true);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get(path);
      if (mounted.current) {
        setData(res.data?.data ?? null);
        setMeta(res.data?.meta ?? null);
      }
    } catch (err) {
      if (mounted.current) setError(apiError(err, "Gagal memuat data"));
    } finally {
      if (mounted.current) setLoading(false);
    }
  }, [path]);

  useEffect(() => {
    mounted.current = true;
    load();
    return () => { mounted.current = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return { data, meta, loading, error, reload: load };
}
