import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../utils/api';
import toast from 'react-hot-toast';

const Collections = () => {
    const [collections, setCollections] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCollections = async () => {
            try {
                const response = await api.get('sunnah/collections/');
                setCollections(response.data);
                setLoading(false);
            } catch (error) {
                console.error("Error fetching collections:", error);
                toast.error("Failed to load collections");
                setLoading(false);
            }
        };

        fetchCollections();
    }, []);

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

            <div className="row">
                <div className="col-12 mb-4">
                    <div className="d-flex justify-content-between align-items-center">
                        <h4 className="card-title mb-0">All Collections</h4>
                        <Link to="/sunnah/search" className="btn btn-primary btn-sm">
                            <i className="fa fa-search me-2"></i>Global Search
                        </Link>
                    </div>
                </div>
                
                {collections.map((collection) => (
                    <div className="col-xl-3 col-lg-4 col-md-6 col-sm-6" key={collection.slug}>
                        <Link to={`/sunnah/${collection.slug}`} className="text-decoration-none">
                            <div className="card text-center text-dark" style={{ transition: 'transform 0.2s', cursor: 'pointer' }} onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-5px)'} onMouseLeave={(e) => e.currentTarget.style.transform = 'none'}>
                                <div className="card-body">
                                    <div className="mb-3">
                                        <i className="la la-book fa-3x text-primary"></i>
                                    </div>
                                    <h4 className="mb-1">{collection.english_title}</h4>
                                    <p className="text-muted fs-4 mb-3" style={{ fontFamily: 'Amiri, serif' }}>{collection.arabic_title}</p>
                                    
                                    <div className="d-flex justify-content-center align-items-center mt-3">
                                        <span className="badge badge-primary light badge-md">
                                            {collection.num_hadith || 0} Hadiths
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Collections;
