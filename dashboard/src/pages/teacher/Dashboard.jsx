import useAuthStore from '../../store/authStore';

const TeacherDashboard = () => {
    return (
        <div className="container-fluid pt-4">
            <h2 className="mb-4">Teacher Dashboard</h2>
            
            <div className="row">
                {/* Stats */}
                <div className="col-xl-3 col-xxl-3 col-sm-6">
                    <div className="widget-stat card bg-primary text-white">
                        <div className="card-body">
                            <div className="media">
                                <span className="me-3"><i className="la la-users fs-1"></i></span>
                                <div className="media-body">
                                    <p className="mb-1">My Students</p>
                                    <h3 className="text-white">24</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-xl-3 col-xxl-3 col-sm-6">
                    <div className="widget-stat card bg-warning text-white">
                        <div className="card-body">
                            <div className="media">
                                <span className="me-3"><i className="la la-calendar fs-1"></i></span>
                                <div className="media-body">
                                    <p className="mb-1">Classes Today</p>
                                    <h3 className="text-white">5</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-xl-3 col-xxl-3 col-sm-6">
                    <div className="widget-stat card bg-secondary text-white">
                        <div className="card-body">
                            <div className="media">
                                <span className="me-3"><i className="la la-pencil fs-1"></i></span>
                                <div className="media-body">
                                    <p className="mb-1">Pending HW</p>
                                    <h3 className="text-white">12</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-xl-3 col-xxl-3 col-sm-6">
                    <div className="widget-stat card bg-danger text-white">
                        <div className="card-body">
                            <div className="media">
                                <span className="me-3"><i className="la la-comment fs-1"></i></span>
                                <div className="media-body">
                                    <p className="mb-1">Unread Chats</p>
                                    <h3 className="text-white">3</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="row">
                {/* Quick Log Form */}
                <div className="col-xl-4 col-lg-12 mb-4">
                    <div className="card h-100">
                        <div className="card-header">
                            <h4 className="card-title">Quick Log Lesson</h4>
                        </div>
                        <div className="card-body">
                            <form>
                                <div className="mb-3">
                                    <label className="form-label">Student</label>
                                    <select className="form-select">
                                        <option>Abdullah (STU-0001)</option>
                                        <option>Fatima (STU-0002)</option>
                                    </select>
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Type</label>
                                    <select className="form-select">
                                        <option>New Memorization</option>
                                        <option>Revision (Mutashabihat)</option>
                                        <option>Reading (Nazra)</option>
                                    </select>
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Range</label>
                                    <input type="text" className="form-control" placeholder="e.g. Al-Baqarah 1-10"/>
                                </div>
                                <button type="button" className="btn btn-primary w-100">Save Log</button>
                            </form>
                        </div>
                    </div>
                </div>

                {/* Schedule & Students Table */}
                <div className="col-xl-8 col-lg-12 mb-4">
                    <div className="card h-100">
                        <div className="card-header">
                            <h4 className="card-title">Today's Schedule</h4>
                        </div>
                        <div className="card-body p-0">
                            <div className="table-responsive">
                                <table className="table table-striped align-middle mb-0">
                                    <thead className="table-light">
                                        <tr>
                                            <th>Time</th>
                                            <th>Student</th>
                                            <th>Meeting</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>04:00 PM</td>
                                            <td>Abdullah (STU-0001)</td>
                                            <td><a href="#" className="text-primary">Meet Link</a></td>
                                            <td>
                                                <button className="btn btn-sm btn-outline-danger me-2" title="Ring Alert">
                                                    <i className="la la-bell"></i>
                                                </button>
                                                <button className="btn btn-sm btn-outline-primary" title="Log Lesson">
                                                    <i className="la la-book"></i>
                                                </button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>04:45 PM</td>
                                            <td>Fatima (STU-0002)</td>
                                            <td><a href="#" className="text-primary">Meet Link</a></td>
                                            <td>
                                                <button className="btn btn-sm btn-outline-danger me-2" title="Ring Alert">
                                                    <i className="la la-bell"></i>
                                                </button>
                                                <button className="btn btn-sm btn-outline-primary" title="Log Lesson">
                                                    <i className="la la-book"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TeacherDashboard;
