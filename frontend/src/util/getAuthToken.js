import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export const getAuthToken = async () => {
  try {
    const response = await axios.post(`${API_URL}/auth/token`, {
      email: "dev@test.com",
      password: "devpass"
    });
    
    if (response.data.access_token) {
      return response.data.access_token;
    }
    throw new Error('No token received');
  } catch (error) {
    console.error('Token request failed:', error.response?.data || error.message);
    throw error;
  }
};