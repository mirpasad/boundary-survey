import { create } from 'zustand';
import axios from 'axios';
import { getAuthToken } from "../util/getAuthToken";

export const useAuthStore = create((set, get) => ({
  token: localStorage.getItem('authToken') || null,
  isLoading: false,
  error: null,
  
  fetchToken: async () => {
    if (get().isLoading) return null;
    
    set({ isLoading: true, error: null });
    
    try {
      const token = await getAuthToken();
      if (token) {
        set({ token });
        localStorage.setItem('authToken', token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        return token;
      }
    } catch (error) {
      set({ error: error.message || 'Failed to get authentication token' });
    } finally {
      set({ isLoading: false });
    }
    return null;
  },
  
  clearToken: () => {
    set({ token: null });
    localStorage.removeItem('authToken');
    delete axios.defaults.headers.common['Authorization'];
  },
  
  isAuthenticated: () => {
    return !!get().token;
  }

import { create } from 'zustand'; // Import create from Zustand
import axios from 'axios'; // Import Axios
import { getAuthToken } from "../util/getAuthToken";

export const useAuthStore = create((set) => ({
  token: localStorage.getItem('authToken') || null,
  isLoading: false,
  error: null,
  
  fetchToken: async () => {
    set({ isLoading: true, error: null });
    
    try {
      const token = await getAuthToken();
      console.log("lol Fetched token:", token);
      if (token) {
        set({ token });
        localStorage.setItem('authToken', token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      }
    } catch (error) {
      set({ error: error.message || 'Failed to get authentication token' });
    } finally {
      set({ isLoading: false });
    }
  },
  
  clearToken: () => {
    set({ token: null });
    localStorage.removeItem('authToken');
    delete axios.defaults.headers.common['Authorization'];
  }
}));