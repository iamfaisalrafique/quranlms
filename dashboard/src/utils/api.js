import axios from 'axios';
import useAuthStore from '../store/authStore';

// Base API instance
const api = axios.create({
    baseURL: '/api/',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request Interceptor: Attach Token
api.interceptors.request.use(
    (config) => {
        const state = useAuthStore.getState();
        const token = state.token?.access; // Assuming token object has { access, refresh }

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response Interceptor: Handle 401 & Token Refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        const state = useAuthStore.getState();

        // If 401 Unauthorized and not already retrying
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            const refresh = state.token?.refresh;
            
            if (refresh) {
                try {
                    // Call Django SimpleJWT refresh endpoint
                    const res = await axios.post('/api/accounts/token/refresh/', {
                        refresh
                    });
                    
                    // Update token in Zustand store
                    const newToken = { access: res.data.access, refresh };
                    state.login(state.user, newToken, state.role);
                    
                    // Retry original request with new token
                    api.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`;
                    return api(originalRequest);
                } catch (refreshError) {
                    // Refresh failed (expired/invalid)
                    state.logout();
                    window.location.href = '/login';
                    return Promise.reject(refreshError);
                }
            } else {
                // No refresh token available
                state.logout();
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;
