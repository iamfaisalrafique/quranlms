import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../utils/api';
import toast from 'react-hot-toast';

const SurahList = () => {
    const [surahs, setSurahs] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        fetchSurahs();
    }, []);

    const fetchSurahs = async () => {
        try {
            // Using the API endpoint created in Session 3
            const response = await api.get('/quran/surahs/');
            setSurahs(response.data);
        } catch (error) {
            toast.error('Failed to load Surahs');
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    const filteredSurahs = surahs.filter(surah => {
        const query = searchQuery.toLowerCase();
        return (
            surah.name_english.toLowerCase().includes(query) ||
            surah.name_arabic.includes(query) ||
            surah.number.toString() === query
        );
    });

    return (
        <div className="container-fluid pt-4">
            <div className="row mb-4">
                <div className="col-12 d-flex justify-content-between align-items-center flex-wrap">
                    <h2 className="mb-3 mb-sm-0">The Noble Quran</h2>
                    <div className="search-area d-flex align-items-center">
                        <div className="input-group search-area">
                            <input 
                                type="text" 
                                className="form-control" 
                                placeholder="Search 'Al-Mulk', '67'..." 
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                            <span className="input-group-text">
                                <i className="la la-search"></i>
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            {isLoading ? (
                <div className="text-center py-5">
                    <div className="spinner-border text-primary" role="status"></div>
                </div>
            ) : (
                <div className="row">
                    {filteredSurahs.map(surah => (
                        <div key={surah.number} className="col-xl-3 col-lg-4 col-md-6 mb-4">
                            <Link to={`/quran/${surah.number}`} className="text-decoration-none">
                                <div className="card h-100 hover-elevate transition-all">
                                    <div className="card-body d-flex align-items-center">
                                        <div className="bg-light text-primary rounded-circle d-flex align-items-center justify-content-center me-3" 
                                             style={{ width: '48px', height: '48px', flexShrink: 0, fontWeight: 'bold' }}>
                                            {surah.number}
                                        </div>
                                        <div className="flex-grow-1">
                                            <h5 className="mb-0 text-dark">{surah.name_english}</h5>
                                            <small className="text-muted">{surah.revelation_type} • {surah.total_ayats} Ayahs</small>
                                        </div>
                                        <div className="text-end">
                                            <h4 className="mb-0 text-primary" style={{ fontFamily: "'KFGQPC Uthmanic Script HAFS', serif" }}>
                                                {surah.name_arabic}
                                            </h4>
                                        </div>
                                    </div>
                                </div>
                            </Link>
                        </div>
                    ))}
                    
                    {filteredSurahs.length === 0 && !isLoading && (
                        <div className="col-12 text-center py-5">
                            <h4 className="text-muted">No Surahs found matching "{searchQuery}"</h4>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default SurahList;
