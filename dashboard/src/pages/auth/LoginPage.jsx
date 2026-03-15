import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../utils/api';
import useAuthStore from '../../store/authStore';
import toast, { Toaster } from 'react-hot-toast';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
    const login = useAuthStore((state) => state.login);

    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const response = await api.post('/accounts/auth/login/', {
                username,
                password
            });
            
            const { access, refresh, user } = response.data;

            // Login with user, token, and role
            login(user, { access, refresh }, user.role);

            // The Switch
            if (user.role === 'admin') {
                navigate('/admin/dashboard');
            } else if (user.role === 'teacher') {
                navigate('/teacher/dashboard');
            } else if (user.role === 'student') {
                navigate('/student/dashboard');
            } else {
                navigate('/dashboard');
            }

        } catch (error) {
            toast.error('Invalid credentials. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleGoogleAuth = () => {
        // Redirect to Django OAuth endpoint
        window.location.href = '/api/accounts/auth/google/';
    };

    return (
        <div className="vh-100 d-flex align-items-center">
            <Toaster position="top-right" />
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-lg-5 col-md-6">
                        <div className="card mb-0 h-auto">
                            <div className="card-body">
                                <div className="text-center mb-4">
                                    <h2 className="text-primary mb-3">IslamicLMS</h2>
                                    <h3>Login</h3>
                                </div>
                                <form onSubmit={handleLogin}>
                                    <div className="form-group mb-3">
                                        <label className="form-label">Username</label>
                                        <input 
                                            type="text"
                                            className="form-control" 
                                            placeholder="admin123"
                                            value={username}
                                            onChange={(e) => setUsername(e.target.value)}
                                            required
                                        />
                                    </div>
                                    <div className="form-group mb-4">
                                        <label className="form-label">Password</label>
                                        <input 
                                            type="password" 
                                            className="form-control" 
                                            placeholder="••••••••" 
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                            required
                                        />
                                    </div>
                                    <div className="text-center mb-3">
                                        <button 
                                            type="submit" 
                                            className="btn btn-primary btn-block w-100"
                                            disabled={isLoading}
                                        >
                                            {isLoading ? 'Signing In...' : 'Sign In'}
                                        </button>
                                    </div>
                                </form>
                                <div className="text-center mt-4 border-top pt-4">
                                    <p className="text-muted">Or sign in with Workspace</p>
                                    <button 
                                        className="btn btn-outline-dark w-100" 
                                        onClick={handleGoogleAuth}
                                    >
                                        <i className="fa fa-google me-2"></i> Continue with Google
                                    </button>
                                </div>
                                <div className="text-center mt-3 pt-3 border-top">
                                    <p className="text-muted">Are you a student?</p>
                                    <button
                                        type="button"
                                        className="btn btn-outline-primary w-100"
                                        onClick={() => navigate('/student/login')}
                                    >
                                        Student Login
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
