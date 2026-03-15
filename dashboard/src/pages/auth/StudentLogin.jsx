import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../../utils/api';
import useAuthStore from '../../store/authStore';
import toast, { Toaster } from 'react-hot-toast';

const StudentLogin = () => {
    const [loginId, setLoginId] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
    const login = useAuthStore((state) => state.login);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Basic Pattern Validation STU-XXXX
        const stuPattern = /^STU-\d{4}$/;
        if (!stuPattern.test(loginId)) {
            toast.error('Invalid ID format. Must be STU-XXXX');
            return;
        }

        setIsLoading(true);
        try {
            // Placeholder endpoint: replace with actual backend endpoint
            const response = await api.post('/accounts/auth/student/login/', {
                student_id: loginId
            });
            
            // Assuming response contains { access, refresh, user: { ... } }
            login(response.data.user, { access: response.data.access, refresh: response.data.refresh }, 'student');
            navigate('/dashboard');
        } catch (error) {
            toast.error(error.response?.data?.detail || error.response?.data?.error || 'Login failed. Please check your ID.');
        } finally {
            setIsLoading(false);
        }
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
                                    <h2 className="text-primary mb-3" style={{ fontFamily: "'Amiri', serif" }}>
                                        بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم
                                    </h2>
                                    <h3>Student Portal</h3>
                                    <p className="text-muted">Enter your academy issued STU-ID</p>
                                </div>
                                <form onSubmit={handleSubmit}>
                                    <div className="form-group mb-4">
                                        <label className="form-label" htmlFor="loginId">Student ID</label>
                                        <input 
                                            type="text" 
                                            className="form-control form-control-lg" 
                                            placeholder="STU-0001" 
                                            id="loginId"
                                            value={loginId}
                                            onChange={(e) => setLoginId(e.target.value.toUpperCase())}
                                            required
                                        />
                                    </div>
                                    <div className="text-center">
                                        <button 
                                            type="submit" 
                                            className="btn btn-primary btn-block btn-lg w-100 mb-3"
                                            disabled={isLoading}
                                        >
                                            {isLoading ? 'Authenticating...' : 'Enter Academy'}
                                        </button>
                                    </div>
                                    <div className="text-center mt-3">
                                        <Link to="/login" className="text-muted">Staff Login</Link>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default StudentLogin;
