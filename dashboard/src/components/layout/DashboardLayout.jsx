import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

const DashboardLayout = () => {
    return (
        <div className="d-flex" style={{ backgroundColor: '#f5f5f9', minHeight: '100vh' }}>
            <Sidebar />
            <div className="content-body flex-grow-1" style={{ marginLeft: '250px', padding: '20px' }}>
                <Outlet />
            </div>
        </div>
    );
};

export default DashboardLayout;
