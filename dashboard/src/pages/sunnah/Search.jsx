import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../utils/api';
import toast from 'react-hot-toast';

const Search = () => {
    const [query, setQuery] = useState('');
    const [collectionFilter, setCollectionFilter] = useState('');
    const [collections, setCollections] = useState([]);
    
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [hasSearched, setHasSearched] = useState(false);

    useEffect(() => {
        // Load collections for the filter dropdown
        const fetchCollections = async () => {
            try {
                const res = await api.get('sunnah/collections/');
                setCollections(res.data);
            } catch (err) {
                console.error("Failed to load collections for filters", err);
            }
        };
        fetchCollections();
    }, []);

    const handleSearch = async (e) => {
        e?.preventDefault();
        if (!query.trim()) {
            toast.error("Please enter a search term");
            return;
        }

        setLoading(true);
        setHasSearched(true);
        
        try {
            let url = `sunnah/search/?q=${encodeURIComponent(query)}`;
            if (collectionFilter) {
                url += `&collection=${collectionFilter}`;
            }
            
            const response = await api.get(url);
            // Handle if paginated or simple list
            setResults(response.data.results || response.data);
        } catch (error) {
            console.error("Search error:", error);
            toast.error("Search failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container-fluid">
            <div className="row page-titles mx-0">
                <div className="col-sm-6 p-md-0">
                    <div className="welcome-text">
                        <h4>Search Sunnah</h4>
                        <p className="mb-0">Search across all authentic hadith collections</p>
                    </div>
                </div>
                <div className="col-sm-6 p-md-0 justify-content-sm-end mt-2 mt-sm-0 d-flex">
                    <ol className="breadcrumb">
                        <li className="breadcrumb-item"><Link to="/dashboard">Dashboard</Link></li>
                        <li className="breadcrumb-item"><Link to="/sunnah">Sunnah</Link></li>
                        <li className="breadcrumb-item active">Search</li>
                    </ol>
                </div>
            </div>

            <div className="row">
                <div className="col-12">
                    <div className="card">
                        <div className="card-body">
                            <form onSubmit={handleSearch}>
                                <div className="row">
                                    <div className="col-lg-8 col-md-12 mb-3">
                                        <div className="input-group search-area">
                                            <input 
                                                type="text" 
                                                className="form-control" 
                                                placeholder="Search by keywords, narrators, or text..."
                                                value={query}
                                                onChange={(e) => setQuery(e.target.value)}
                                            />
                                        </div>
                                    </div>
                                    <div className="col-lg-3 col-md-8 mb-3">
                                        <select 
                                            className="form-control default-select" 
                                            value={collectionFilter}
                                            onChange={(e) => setCollectionFilter(e.target.value)}
                                        >
                                            <option value="">All Collections</option>
                                            {collections.map(c => (
                                                <option key={c.slug} value={c.slug}>
                                                    {c.title_en || c.name}
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                    <div className="col-lg-1 col-md-4 mb-3">
                                        <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                                            {loading ? <i className="fa fa-spinner fa-spin"></i> : <i className="flaticon-381-search-2"></i>}
                                        </button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <div className="row">
                <div className="col-12">
                    {loading && (
                        <div className="text-center my-5">
                            <div className="spinner-border text-primary" role="status"></div>
                        </div>
                    )}

                    {!loading && hasSearched && results.length === 0 && (
                        <div className="alert alert-info text-center">
                            No hadiths matched your search query. Try different keywords.
                        </div>
                    )}

                    {!loading && results.length > 0 && (
                        <div className="card">
                            <div className="card-header border-0 pb-0">
                                <h4 className="card-title">Search Results ({results.length})</h4>
                            </div>
                            <div className="card-body">
                                <ul className="list-group list-group-flush">
                                    {results.map((result) => {
                                        // Sometimes searches return nested objects depending on DRF setup
                                        // Allow robust mapping
                                        const slug = result.collection?.slug || result.collection_slug;
                                        const book = result.book?.book_number || result.book_number;
                                        const num = result.hadith_number;
                                        
                                        return (
                                            <li className="list-group-item px-0 py-4" key={result.id}>
                                                <div className="d-flex justify-content-between align-items-start border-bottom pb-4 mb-3">
                                                    <div>
                                                        <Link to={`/sunnah/${slug}/book/${book}?highlight=${encodeURIComponent(query)}`} className="text-decoration-none">
                                                            <h5 className="text-primary mb-2 hover-underline">
                                                                {result.collection?.name || result.collection_name} — Book {book}, Hadith {num}
                                                            </h5>
                                                        </Link>
                                                        
                                                        {result.grade && (
                                                            <span className="badge badge-light text-dark mb-3">
                                                                Grade: {result.grade}
                                                            </span>
                                                        )}
                                                        
                                                        <p className="mb-3 text-dark fs-5" dangerouslySetInnerHTML={{ __html: result.body_en ? (result.body_en.length > 300 ? result.body_en.substring(0, 300) + '...' : result.body_en) : 'No English translation available.' }} />
                                                    </div>
                                                    
                                                    <div className="w-50 text-end ms-4" style={{ direction: 'rtl' }}>
                                                        <p className="text-dark" style={{ fontFamily: 'Amiri, serif', fontSize: '1.4rem', lineHeight: '2' }} dangerouslySetInnerHTML={{ __html: result.body_ar ? (result.body_ar.length > 300 ? result.body_ar.substring(0, 300) + '...' : result.body_ar) : '' }} />
                                                    </div>
                                                </div>
                                            </li>
                                        );
                                    })}
                                </ul>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Search;
