import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../utils/api';
import toast from 'react-hot-toast';

const Search = () => {
    const [query, setQuery] = useState('');
    const [selectedCollections, setSelectedCollections] = useState([]);
    const [collections, setCollections] = useState([]);
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [hasSearched, setHasSearched] = useState(false);
    const [totalResults, setTotalResults] = useState(0);
    const [currentPage, setCurrentPage] = useState(1);

    useEffect(() => {
        const fetchCollections = async () => {
            try {
                const res = await api.get('sunnah/collections/');
                setCollections(res.data);
            } catch (err) {
                console.error("Failed to load collections", err);
            }
        };
        fetchCollections();
    }, []);

    const handleSearch = async (e, page = 1) => {
        e?.preventDefault();
        if (!query.trim()) {
            toast.error("Please enter a search term");
            return;
        }

        setLoading(true);
        setHasSearched(true);
        setCurrentPage(page);
        
        try {
            let url = `sunnah/search/?q=${encodeURIComponent(query)}&page=${page}`;
            if (selectedCollections.length > 0) {
                // Assuming backend can handle comma-separated slugs or multiple params
                url += `&collections=${selectedCollections.join(',')}`;
            }
            
            const response = await api.get(url);
            setResults(response.data.results || []);
            setTotalResults(response.data.count || 0);
            window.scrollTo(0, 0);
        } catch (error) {
            console.error("Search error:", error);
            toast.error("Search failed");
        } finally {
            setLoading(false);
        }
    };

    const toggleCollection = (slug) => {
        setSelectedCollections(prev =>
            prev.includes(slug) ? prev.filter(s => s !== slug) : [...prev, slug]
        );
    };

    const highlightText = (text, highlight) => {
        if (!highlight.trim()) return text;
        const parts = text.split(new RegExp(`(${highlight})`, 'gi'));
        return (
            <span>
                {parts.map((part, i) =>
                    part.toLowerCase() === highlight.toLowerCase()
                        ? <span key={i} style={{ backgroundColor: '#D4AF37', color: 'black', padding: '0 2px', borderRadius: '2px' }}>{part}</span>
                        : part
                )}
            </span>
        );
    };

    const totalPages = Math.ceil(totalResults / 20);

    return (
        <div className="container-fluid">
            <div className="row page-titles mx-0">
                <div className="col-sm-6 p-md-0">
                    <div className="welcome-text">
                        <h4>Global Search</h4>
                        <p className="mb-0">Find hadiths across all collections</p>
                    </div>
                </div>
                <div className="col-sm-6 p-md-0 justify-content-sm-end mt-2 mt-sm-0 d-flex">
                    <ol className="breadcrumb">
                        <li className="breadcrumb-item"><Link to="/sunnah">Sunnah</Link></li>
                        <li className="breadcrumb-item active">Search</li>
                    </ol>
                </div>
            </div>

            <div className="row mb-4">
                <div className="col-lg-10 mx-auto">
                    <div className="card shadow-sm border-0 p-4" style={{ borderRadius: '1rem' }}>
                        <form onSubmit={(e) => handleSearch(e, 1)}>
                            <div className="input-group input-group-lg">
                                <span className="input-group-text bg-white border-end-0">
                                    <i className="fa fa-search text-success"></i>
                                </span>
                                <input
                                    type="text"
                                    className="form-control border-start-0 shadow-none"
                                    placeholder="Search by keywords, narrators, or text..."
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    style={{ fontSize: '1.25rem' }}
                                />
                                <button type="submit" className="btn btn-primary px-5" style={{ backgroundColor: '#1A6B4A', border: 'none' }} disabled={loading}>
                                    {loading ? <i className="fa fa-spinner fa-spin"></i> : "Search"}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            <div className="row">
                {/* Sidebar Filters */}
                <div className="col-xl-3 col-lg-4">
                    <div className="card shadow-sm border-0" style={{ borderRadius: '1rem' }}>
                        <div className="card-header bg-white border-bottom py-3">
                            <h5 className="mb-0 fw-bold">Filter by Collection</h5>
                        </div>
                        <div className="card-body p-0" style={{ maxHeight: '600px', overflowY: 'auto' }}>
                            <div className="list-group list-group-flush">
                                {collections.map(c => (
                                    <label key={c.slug} className="list-group-item border-0 py-3 px-4 d-flex align-items-center cursor-pointer">
                                        <input
                                            type="checkbox"
                                            className="form-check-input me-3"
                                            checked={selectedCollections.includes(c.slug)}
                                            onChange={() => toggleCollection(c.slug)}
                                            style={{ cursor: 'pointer', width: '20px', height: '20px' }}
                                        />
                                        <span className="text-dark">{c.english_title}</span>
                                    </label>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Search Results */}
                <div className="col-xl-9 col-lg-8">
                    {hasSearched && (
                        <div className="mb-4">
                            <h5 className="text-muted">
                                {totalResults.toLocaleString()} results found for <strong>"{query}"</strong>
                            </h5>
                        </div>
                    )}

                    {loading && (
                        <div className="text-center my-5">
                            <div className="spinner-border text-success" role="status" style={{ width: '3rem', height: '3rem' }}></div>
                        </div>
                    )}

                    {!loading && results.map((result) => (
                        <div className="card mb-4 result-card shadow-sm border-0 overflow-hidden" key={result.id} style={{ borderRadius: '1rem' }}>
                            <div className="card-body p-0">
                                <div className="p-4">
                                    <div className="d-flex justify-content-between align-items-start mb-3">
                                        <div>
                                            <span className="badge me-2" style={{ backgroundColor: 'rgba(26, 107, 74, 0.1)', color: '#1A6B4A' }}>
                                                {result.collection_title}
                                            </span>
                                            <span className="text-muted small">Book {result.book_number}, Hadith {result.hadith_number}</span>
                                        </div>
                                        <Link to={`/sunnah/${result.collection_slug}/book/${result.book_number}`} className="btn btn-sm btn-outline-success rounded-pill px-3">
                                            View Context
                                        </Link>
                                    </div>

                                    <div className="row">
                                        <div className="col-md-6 border-end">
                                            <div className="text-muted small mb-1">English Translation</div>
                                            <p className="text-dark mb-0" style={{ fontSize: '1rem', lineHeight: '1.6' }}>
                                                {highlightText(result.english_body.substring(0, 300) + (result.english_body.length > 300 ? '...' : ''), query)}
                                            </p>
                                        </div>
                                        <div className="col-md-6 mt-3 mt-md-0">
                                            <div className="text-muted small mb-1 text-end">Arabic Text</div>
                                            <p className="text-end mb-0" style={{ fontFamily: 'Amiri, serif', fontSize: '1.3rem', lineHeight: '2', direction: 'rtl' }}>
                                                {result.arabic_body.substring(0, 200) + (result.arabic_body.length > 200 ? '...' : '')}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}

                    {!loading && hasSearched && results.length === 0 && (
                        <div className="alert alert-light text-center border p-5">
                            <i className="la la-search fa-3x text-muted mb-3"></i>
                            <h4>No results found</h4>
                            <p>Try adjusting your search terms or filters.</p>
                        </div>
                    )}

                    {/* Pagination */}
                    {totalPages > 1 && (
                        <nav className="d-flex justify-content-center mt-5">
                            <ul className="pagination pagination-primary pagination-gutter">
                                <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                                    <button className="page-link" onClick={() => handleSearch(null, currentPage - 1)}>
                                        <i className="la la-angle-left"></i>
                                    </button>
                                </li>
                                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                                    let pNum;
                                    if (totalPages <= 5) pNum = i + 1;
                                    else if (currentPage <= 3) pNum = i + 1;
                                    else if (currentPage >= totalPages - 2) pNum = totalPages - 4 + i;
                                    else pNum = currentPage - 2 + i;

                                    return (
                                        <li key={pNum} className={`page-item ${currentPage === pNum ? 'active' : ''}`}>
                                            <button className="page-link" onClick={() => handleSearch(null, pNum)}>{pNum}</button>
                                        </li>
                                    );
                                })}
                                <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
                                    <button className="page-link" onClick={() => handleSearch(null, currentPage + 1)}>
                                        <i className="la la-angle-right"></i>
                                    </button>
                                </li>
                            </ul>
                        </nav>
                    )}
                </div>
            </div>

            <style dangerouslySetInnerHTML={{ __html: `
                .result-card {
                    transition: transform 0.2s;
                }
                .result-card:hover {
                    transform: translateY(-3px);
                }
                .cursor-pointer {
                    cursor: pointer;
                }
                .pagination-primary .page-item.active .page-link {
                    background-color: #1A6B4A!important;
                    border-color: #1A6B4A!important;
                }
            `}} />
        </div>
    );
};

export default Search;
