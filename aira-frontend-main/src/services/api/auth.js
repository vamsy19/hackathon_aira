import axios from 'axios';

const API_URL = 'http://localhost:8000/';  // Adjust based on your Django server URL

const login = async (username, password) => {
    try {
        const response = await axios.post(`${API_URL}authentication/api/token/`, {
            username,
            password
        });
        return response.data;
    } catch (error) {
        console.error('Login failed:', error);
        throw error;
    }
};

export { login };
