import { Routes, Route, Navigate } from 'react-router-dom';

import { useEffect } from 'react';
import LoginPage from './pages/auth/LoginPage';
import StudentLogin from './pages/auth/StudentLogin';
import DashboardLayout from './components/layout/DashboardLayout';
import StudentDashboard from './pages/student/Dashboard';
import TeacherDashboard from './pages/teacher/Dashboard';

import SurahList from './pages/quran/SurahList';
import QuranViewer from './pages/quran/QuranViewer';

import Collections from './pages/sunnah/Collections';
import BookList from './pages/sunnah/BookList';
import HadithList from './pages/sunnah/HadithList';
import Search from './pages/sunnah/Search';

import useAuthStore from './store/authStore';

// Protected route logic utilizing Zustand store
const ProtectedRoute = ({ children, allowedRoles }) => {
  const { isAuthenticated, role, isAuthLoading } = useAuthStore();
  
  if (isAuthLoading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
     // If user is authenticated but not allowed for this route, redirect based on their role
     if (role === 'admin') return <Navigate to="/admin/dashboard" replace />;
     if (role === 'teacher') return <Navigate to="/teacher/dashboard" replace />;
     if (role === 'student') return <Navigate to="/student/dashboard" replace />;
     return <Navigate to="/dashboard" replace />;
  }
  
  return children;
};

// Placeholder AdminDashboard if it doesn't exist
const AdminDashboard = () => <div>Admin Dashboard (Placeholder)</div>;

function App() {
  const checkAuth = useAuthStore((state) => state.checkAuth);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/student/login" element={<StudentLogin />} />
      
      {/* Protected Layout Boundaries */}
      <Route element={<DashboardLayout />}>
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute allowedRoles={['student']}>
                <StudentDashboard />
              </ProtectedRoute>
            } 
          />
          <Route
            path="/student/dashboard"
            element={
              <ProtectedRoute allowedRoles={['student']}>
                <StudentDashboard />
              </ProtectedRoute>
            }
          />
          <Route 
            path="/teacher/dashboard" 
            element={
              <ProtectedRoute allowedRoles={['teacher']}>
                <TeacherDashboard />
              </ProtectedRoute>
            } 
          />
          <Route
            path="/admin/dashboard"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route path="/quran" element={<ProtectedRoute><SurahList /></ProtectedRoute>} />
          <Route path="/quran/:surahId" element={<ProtectedRoute><QuranViewer /></ProtectedRoute>} />

          {/* Sunnah Routes */}
          <Route path="/sunnah" element={<ProtectedRoute><Collections /></ProtectedRoute>} />
          <Route path="/sunnah/search" element={<ProtectedRoute><Search /></ProtectedRoute>} />
          <Route path="/sunnah/:slug" element={<ProtectedRoute><BookList /></ProtectedRoute>} />
          <Route path="/sunnah/:slug/book/:bookNum" element={<ProtectedRoute><HadithList /></ProtectedRoute>} />
      </Route>
    </Routes>
  )
}

export default App;
