import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

const useAuthStore = create(
    devtools(
        persist(
            (set) => ({
                user: null,
                token: null,
                role: null, // 'student' | 'teacher' | 'admin'
                isAuthenticated: false,
                isLoading: false,
                isAuthLoading: true,

                login: (user, token, role) => set({
                    user,
                    token,
                    role,
                    isAuthenticated: true,
                    isLoading: false,
                    isAuthLoading: false
                }),

                logout: () => set({
                    user: null,
                    token: null,
                    role: null,
                    isAuthenticated: false,
                    isLoading: false,
                    isAuthLoading: false
                }),

                setLoading: (isLoading) => set({ isLoading }),
                setAuthLoading: (isAuthLoading) => set({ isAuthLoading }),

                checkAuth: async () => {
                    set({ isAuthLoading: true });
                    try {
                        // In a real app, verify token with backend here
                        // For now, we rely on the persisted state but add a small delay
                        await new Promise(resolve => setTimeout(resolve, 300));
                    } finally {
                        set({ isAuthLoading: false });
                    }
                }
            }),
            {
                name: 'auth-storage', // saves to localStorage
            }
        )
    )
);

export default useAuthStore;
