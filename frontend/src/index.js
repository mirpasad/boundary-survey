// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { useAuthStore } from './authStore';

const root = ReactDOM.createRoot(document.getElementById('root'));

(async function init() {
  try {
    const { token, fetchToken } = useAuthStore.getState();
    if (!token) {
      await fetchToken();
    }
  } catch (e) {
    console.error('Failed to prefetch token:', e);
  } finally {
    root.render(<App />);
  }
})();
