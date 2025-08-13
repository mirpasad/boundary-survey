// getAuthToken.js
import axios from 'axios';

// In development, leave REACT_APP_BACKEND_URL empty to use CRA proxy.
// In production, set REACT_APP_BACKEND_URL to your API origin, e.g. https://api.example.com
const API_BASE = process.env.REACT_APP_BACKEND_URL || ''; // '' => uses proxy in dev

// Dev login credentials (override via env in production)
const DEV_EMAIL = process.env.REACT_APP_DEV_LOGIN_EMAIL || 'dev@test.com';
const DEV_PASSWORD = process.env.REACT_APP_DEV_LOGIN_PASSWORD || 'devpass';

/**
 * Requests a JWT from the backend dev-login endpoint and returns the token string.
 * Throws with a clear message if the request fails or the token is missing.
 */
export default async function getAuthToken() {
  try {
    const res = await axios.post(
      `${API_BASE}/api/auth/token`,
      { email: DEV_EMAIL, password: DEV_PASSWORD },
      { headers: { 'Content-Type': 'application/json' }, timeout: 15000 }
    );

    const token = res?.data?.access_token;
    if (!token) {
      const body = typeof res?.data === 'object' ? JSON.stringify(res.data) : String(res?.data);
      throw new Error(`Auth response missing access_token. Body: ${body}`);
    }
    return token;
  } catch (err) {
    // Surface a helpful error for the caller (auth store) to handle
    if (err?.response) {
      const status = err.response.status;
      const body = typeof err.response.data === 'object'
        ? JSON.stringify(err.response.data)
        : String(err.response.data || err.message);
      throw new Error(`Auth failed (${status}): ${body}`);
    }
    throw err;
  }
}
