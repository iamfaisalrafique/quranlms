import useAuthStore from '../../store/authStore';

const StudentDashboard = () => {
    const user = useAuthStore((state) => state.user);

    return (
        <div className="container-fluid pt-4">
            <h2 className="mb-4">Welcome back, {user?.name || 'Talib'}!</h2>
            
            <div className="row">
                {/* Streak Card */}
                <div className="col-xl-3 col-md-6 col-lg-3 mb-4">
                    <div className="card h-100 bg-primary text-white text-center">
                        <div className="card-body">
                            <h3 className="text-white mb-2">🔥 12 Days</h3>
                            <p className="mb-0">Current Streak</p>
                            <small>Longest: 35 days</small>
                        </div>
                    </div>
                </div>

                {/* Today Class */}
                <div className="col-xl-9 col-md-6 col-lg-9 mb-4">
                    <div className="card h-100">
                        <div className="card-body d-flex justify-content-between align-items-center flex-wrap">
                            <div>
                                <h4 className="card-title text-primary">Next Class: Quran Memorization</h4>
                                <p className="mb-1 text-muted">With Ustadha Aisha • Today, 4:00 PM</p>
                                <span className="badge bg-warning text-dark"><i className="la la-clock me-1"></i>Starts in 45 mins</span>
                            </div>
                            <button className="btn btn-primary btn-lg px-5 mt-2 mt-sm-0">Join Link</button>
                        </div>
                    </div>
                </div>
            </div>

            <div className="row">
                {/* Active Quiz / Pending Tasks */}
                <div className="col-xl-6 col-md-6 col-lg-6 mb-4">
                    <div className="card h-100">
                        <div className="card-header border-0 pb-0">
                            <h4 className="card-title">Pending Tasks</h4>
                        </div>
                        <div className="card-body">
                            <div className="d-flex border-bottom pb-3 mb-3 justify-content-between align-items-center">
                                <div>
                                    <h5 className="mb-1">Surah Al-Mulk Quiz</h5>
                                    <p className="mb-0 fs-14">Assigned by Ustadha Aisha</p>
                                </div>
                                <button className="btn btn-outline-primary btn-sm">Take Quiz</button>
                            </div>
                            <div className="d-flex justify-content-between align-items-center">
                                <div>
                                    <h5 className="mb-1">Memorize Ayah 1-5 (Al-Baqarah)</h5>
                                    <p className="mb-0 fs-14 text-danger">Due: Tomorrow</p>
                                </div>
                                <button className="btn btn-outline-success btn-sm">Mark Done</button>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Badges */}
                <div className="col-xl-6 col-md-6 col-lg-6 mb-4">
                    <div className="card h-100">
                        <div className="card-header border-0 pb-0">
                            <h4 className="card-title">My Achievements</h4>
                        </div>
                        <div className="card-body">
                            <div className="d-flex gap-3 flex-wrap">
                                <div className="text-center p-3 border rounded bg-light" style={{ width: '100px' }}>
                                    <h2 className="mb-1">📖</h2>
                                    <small>First Lesson</small>
                                </div>
                                <div className="text-center p-3 border rounded bg-light" style={{ width: '100px' }}>
                                    <h2 className="mb-1">💯</h2>
                                    <small>Perfect Score</small>
                                </div>
                                <div className="text-center p-3 border rounded bg-light" style={{ width: '100px' }}>
                                    <h2 className="mb-1">🔥</h2>
                                    <small>7-Day Streak</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Lesson History Table (Consolidated) */}
            <div className="row">
                <div className="col-12">
                    <div className="card">
                        <div className="card-header d-flex justify-content-between align-items-center">
                            <h4 className="card-title">Lesson History & Daily Overview</h4>
                            <div className="d-flex gap-2">
                                <button className="btn btn-sm btn-outline-primary">Export PDF</button>
                                <button className="btn btn-sm btn-primary">View Full Log</button>
                            </div>
                        </div>
                        <div className="card-body p-0">
                            <div className="table-responsive">
                                <table className="table mb-0 table-striped">
                                    <thead className="table-light">
                                        <tr>
                                            <th>Date</th>
                                            <th>Type</th>
                                            <th>Topic / Range</th>
                                            <th>Attendance</th>
                                            <th>Grade</th>
                                            <th>Remarks</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Oct 15, 2023</td>
                                            <td><span className="badge bg-primary">Memorization</span></td>
                                            <td>Al-Mulk: 1-10</td>
                                            <td><span className="text-success">Present</span></td>
                                            <td>A+</td>
                                            <td>Excellent tajweed mashAllah.</td>
                                        </tr>
                                        <tr>
                                            <td>Oct 14, 2023</td>
                                            <td><span className="badge bg-secondary">Revision</span></td>
                                            <td>Al-Waqi'ah</td>
                                            <td><span className="text-success">Present</span></td>
                                            <td>A</td>
                                            <td>Needs work on Ghunnah.</td>
                                        </tr>
                                        <tr>
                                            <td>Oct 13, 2023</td>
                                            <td><span className="badge bg-info">Tajweed</span></td>
                                            <td>Noon Sakinah Rules</td>
                                            <td><span className="text-warning">Late (5m)</span></td>
                                            <td>B+</td>
                                            <td>Good progress, keep practicing.</td>
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

export default StudentDashboard;
