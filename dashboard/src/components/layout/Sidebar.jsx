import { Link, useLocation } from 'react-router-dom';
import useAuthStore from '../../store/authStore';

const Sidebar = () => {
    const location = useLocation();
    const role = useAuthStore((state) => state.role);
    const logout = useAuthStore((state) => state.logout);

    const isStudent = role === 'student';

    const menuItems = isStudent ? [
        { title: 'Dashboard', icon: 'la la-home', path: '/dashboard' },
        { title: 'Quran', icon: 'la la-book', path: '/quran' },
        { title: 'Sunnah', icon: 'la la-star', path: '/sunnah' },
        { title: 'Classes', icon: 'la la-calendar', path: '/classes' },
        { title: 'Homework', icon: 'la la-pencil', path: '/homework' },
        { title: 'Quiz', icon: 'la la-question-circle', path: '/quiz' },
        { title: 'Chat', icon: 'la la-comment', path: '/chat' },
        { title: 'Profile', icon: 'la la-user', path: '/profile' }
    ] : [
        { title: 'Dashboard', icon: 'la la-home', path: '/teacher/dashboard' },
        { title: 'Students', icon: 'la la-users', path: '/teacher/students' },
        { title: 'Lessons', icon: 'la la-book-open', path: '/teacher/lessons' },
        { title: 'Classes', icon: 'la la-calendar', path: '/teacher/classes' },
        { title: 'Chat', icon: 'la la-comment', path: '/chat' },
        { title: 'Quiz', icon: 'la la-question-circle', path: '/teacher/quiz' },
        { title: 'Reports', icon: 'la la-bar-chart', path: '/teacher/reports' }
    ];

    return (
        <div className="dlabnav border-end h-100" style={{ width: '250px', position: 'fixed', top: 0, left: 0, overflowY: 'auto', backgroundColor: '#fff', paddingTop: '20px' }}>
            <div className="text-center mb-4">
                <h4 className="text-primary fw-bold" style={{ fontSize: '24px' }}>IslamicLMS</h4>
            </div>
            <div className="dlabnav-scroll">
                <ul className="metismenu px-0" id="menu" style={{ listStyleType: 'none' }}>
                    <li className="nav-label px-4 mb-2 text-uppercase text-muted" style={{ fontSize: '0.75rem', letterSpacing: '1px' }}>Main Menu</li>
                    
                    {menuItems.map((item, index) => {
                        const activePattern = item.title === 'Quran' ? '/quran' : (item.title === 'Sunnah' ? '/sunnah' : item.path);
                        const isActive = location.pathname === activePattern || location.pathname.startsWith(`${activePattern}/`);

                        return (
                            <li key={index} className={`mb-1 ${isActive ? 'active' : ''}`}>
                                <Link 
                                    to={item.path} 
                                    className={`d-flex align-items-center py-2 px-4 text-decoration-none ${isActive ? 'bg-primary text-white' : 'text-dark'}`}
                                    style={{ transition: 'all 0.3s ease', borderRadius: '0 25px 25px 0', marginRight: '1rem' }}
                                >
                                    <i className={`${item.icon} fs-4 me-3`}></i>
                                    <span className="nav-text fw-medium">{item.title}</span>
                                </Link>
                            </li>
                        );
                    })}
                    
                    <li className="mt-auto px-4 pt-4">
                        <button 
                            onClick={() => logout()}
                            className="btn btn-outline-danger w-100"
                        >
                            <i className="la la-sign-out me-2"></i> Logout
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    );
};

export default Sidebar;
