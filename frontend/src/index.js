import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import { useAuthStore } from './store/authStore';

const root = ReactDOM.createRoot(document.getElementById('root'));

const initApp = async () => {
  try {
    // Try to fetch token if we don't have one
    if (!useAuthStore.getState().token) {
      await useAuthStore.getState().fetchToken();
    }
  } catch (e) {
    console.error('Initial auth failed:', e);
  }
  
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
};

initApp();