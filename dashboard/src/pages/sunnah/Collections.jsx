import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../utils/api';
import toast from 'react-hot-toast';

const Collections = () => {
    const [collections, setCollections] = useState([]);
    const [filteredCollections, setFilteredCollections] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchCollections = async () => {
            try {
                const response = await api.get('sunnah/collections/');
                setCollections(response.data);
                setFilteredCollections(response.data);
                setLoading(false);
            } catch (error) {
                console.error("Error fetching collections:", error);
                toast.error("Failed to load collections");
                setLoading(false);
            }
        };

        fetchCollections();
    }, []);

    useEffect(() => {
        const results = collections.filter(c =>
            c.english_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.arabic_title.includes(searchTerm)
        );
        setFilteredCollections(results);
    }, [searchTerm, collections]);

    if (loading) {
        return (
            <div className="container-fluid d-flex justify-content-center align-items-center" style={{ minHeight: '60vh' }}>
                <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    return (
        <div className="container-fluid">
            <div className="row page-titles mx-0">
                <div className="col-sm-6 p-md-0">
                    <div className="welcome-text">
                        <h4>Hadith Collections</h4>
                        <p className="mb-0">Browse through authentic words of the Prophet ﷺ</p>
                    </div>
                </div>
                <div className="col-sm-6 p-md-0 justify-content-sm-end mt-2 mt-sm-0 d-flex">
                    <ol className="breadcrumb">
                        <li className="breadcrumb-item"><Link to="/dashboard">Dashboard</Link></li>       
                        <li className="breadcrumb-item active"><Link to="/sunnah">Sunnah</Link></li>      
                    </ol>
                </div>
            </div>

            <div className="row mb-5">
                <div className="col-lg-8 mx-auto">
                    <div className="card shadow-sm border-0" style={{ borderRadius: '1rem' }}>
                        <div className="card-body p-4">
                            <div className="input-group">
                                <span className="input-group-text bg-transparent border-end-0">
                                    <i className="fa fa-search text-muted"></i>
                                </span>
                                <input
                                    type="text"
                                    className="form-control border-start-0 py-3 shadow-none"
                                    placeholder="Search collections by name..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    style={{ fontSize: '1.1rem' }}
                                />
                                <Link to="/sunnah/search" className="btn btn-primary px-4 d-flex align-items-center" style={{ backgroundColor: '#1A6B4A', borderColor: '#1A6B4A' }}>
                                    Global Search
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="row">
                {filteredCollections.map((collection) => (
                    <div className="col-xl-3 col-lg-4 col-md-6 col-sm-6 mb-4" key={collection.slug}>      
                        <Link to={/sunnah/\} className="text-decoration-none h-100 d-block">
                            <div className="card text-center h-100 collection-card shadow-sm border-0"    
                                 style={{
                                     borderRadius: '0.75rem',
                                     transition: 'all 0.3s ease',
                                 }}
                            >
                                <div className="card-body d-flex flex-column p-4">
                                    <div className="mb-3 text-end" style={{ direction: 'rtl' }}>
                                        <h3 className="mb-1 text-dark" style={{ fontFamily: 'Amiri, serif', fontSize: '1.8rem', color: '#1A6B4A' }}>
                                            {collection.arabic_title}
                                        </h3>
                                    </div>
                                    <div className="text-start">
                                        <h5 className="fw-bold text-dark mb-2">{collection.english_title}</h5>
                                        <p className="small text-muted mb-3" style={{
                                            display: '-webkit-box',
                                            WebkitLineClamp: '2',
                                            WebkitBoxOrient: 'vertical',
                                            overflow: 'hidden',
                                            minHeight: '2.5rem'
                                        }}>
                                            {collection.short_intro}
                                        </p>
                                    </div>

                                    <div className="mt-auto d-flex justify-content-between align-items-center">
                                        <span className="badge rounded-pill" style={{ backgroundColor: '#1A6B4A', color: 'white', fontWeight: '500' }}>
                                            {collection.num_hadith} Hadiths     
                                        </span>
                                        <span className={adge \}>
                                            {collection.status === 'complete' ? 'Complete' : 'Incomplete'}
                                        </span>
                                    </div>

                                    <div className="browse-overlay position-absolute top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center rounded-3"
                                         style={{
                                             backgroundColor: 'rgba(26, 107, 74, 0.05)',
                                             opacity: 0,
                                             transition: 'opacity 0.3s ease',
                                             border: '2px solid #1A6B4A'
                                         }}>
                                        <span className="btn btn-primary btn-sm rounded-pill px-4 shadow" style={{ backgroundColor: '#1A6B4A', borderColor: '#1A6B4A' }}>Browse</span>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    </div>
                ))}

                {filteredCollections.length === 0 && (
                    <div className="col-12 text-center my-5">
                        <div className="alert alert-light border shadow-sm">
                            <i className="fa fa-info-circle me-2"></i> No collections matched your search.
                        </div>
                    </div>
                )}
            </div>

            <style dangerouslySetInnerHTML={{ __html: 
                .collection-card:hover {
                    transform: translateY(-8px);
                    box-shadow: 0 1rem 3rem rgba(0,0,0,.175)!important;
                }
                .collection-card:hover .browse-overlay {
                    opacity: 1!important;
                }
            }} />
        </div>
    );
};

export default Collections;
