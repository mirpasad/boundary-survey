import axios from 'axios';
import { useAuthStore } from './authStore';

const baseURL = process.env.REACT_APP_BACKEND_URL || '';
const api = axios.create({ baseURL, timeout: 15000 });

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { response, config } = error || {};
    if (response && response.status === 401 && config && !config._retry) {
      try {
        config._retry = true;
        await useAuthStore.getState().fetchToken();
        const token = useAuthStore.getState().token;
        if (token) {
          config.headers = config.headers || {};
          config.headers.Authorization = `Bearer ${token}`;
        }
        return api(config);
      } catch {
        useAuthStore.getState().clearToken();
      }
    }
    return Promise.reject(error);
  }
);

export default api;
