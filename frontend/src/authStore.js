import { create } from 'zustand';
import getAuthToken from './getAuthToken';

export const useAuthStore = create((set, get) => ({
  token: localStorage.getItem('token') || null,
  isLoading: false,
  error: null,

  fetchToken: async () => {
    if (get().isLoading) return get().token;
    try {
      set({ isLoading: true, error: null });
      const token = await getAuthToken();
      localStorage.setItem('token', token);
      set({ token, isLoading: false });
      return token;
    } catch (err) {
      console.error('fetchToken error:', err);
      set({ error: 'Failed to obtain token', isLoading: false });
      throw err;
    }
  },

  clearToken: () => {
    localStorage.removeItem('token');
    set({ token: null, error: null });
  },

  isAuthenticated: () => !!get().token,
}));
