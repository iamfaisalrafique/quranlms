import React, { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import api from '../../utils/api';
import toast from 'react-hot-toast';

const HadithList = () => {
    const { slug, bookNum } = useParams();
    const navigate = useNavigate();
    const [hadiths, setHadiths] = useState([]);
    const [loading, setLoading] = useState(true);
    const [pageInfo, setPageInfo] = useState({ count: 0, next: null, previous: null, current: 1 });







    const [bookmarks, setBookmarks] = useState(new Set());
    const [books, setBooks] = useState([]);
    const [collection, setCollection] = useState(null);
    const [viewLanguage, setViewLanguage] = useState('both'); // 'arabic', 'english', 'both'
    const [jumpPage, setJumpPage] = useState('');

    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                const [colRes, booksRes] = await Promise.all([
                    api.get(`sunnah/${slug}/`),
                    api.get(`sunnah/${slug}/books/`)
                ]);
                setCollection(colRes.data);
                setBooks(booksRes.data);
            } catch (err) {
                console.error("Failed to load collection data", err);
            }
        };
        fetchInitialData();
    }, [slug]);

    useEffect(() => {
        fetchHadiths(`sunnah/${slug}/${bookNum}/hadiths/?page=${pageInfo.current}`);
        fetchBookmarks();
    }, [slug, bookNum, pageInfo.current]);

    const fetchHadiths = async (url) => {
        setLoading(true);
        try {
            const response = await api.get(url);
            setHadiths(response.data.results || []);
            setPageInfo(prev => ({
                ...prev,
                count: response.data.count,
                next: response.data.next,
                previous: response.data.previous
            }));
            window.scrollTo(0, 0);
        } catch (error) {
            console.error("Error fetching hadiths:", error);
            toast.error("Failed to load hadiths");
        } finally {
            setLoading(false);
        }
    };

    const fetchBookmarks = async () => {
        try {
            const res = await api.get('sunnah/bookmarks/');
            const bms = new Set(res.data.map(b => b.hadith_id));
            setBookmarks(bms);
        } catch (error) {
            console.warn("Bookmarks could not be loaded", error);
        }
    };

    const toggleBookmark = async (hadithId) => {
        try {
            if (bookmarks.has(hadithId)) {
                const res = await api.get('sunnah/bookmarks/');
                const bm = res.data.find(b => b.hadith_id === hadithId);
                if (bm) {
                    await api.delete(`sunnah/bookmark/${bm.id}/`);
                    setBookmarks(prev => {
                        const newSet = new Set(prev);
                        newSet.delete(hadithId);
                        return newSet;
                    });
                    toast.success("Bookmark removed");
                }
            } else {
                await api.post('sunnah/bookmark/', { hadith_id: hadithId });
                setBookmarks(prev => new Set([...prev, hadithId]));
                toast.success("Bookmark added");
            }
        } catch (error) {
            console.error(error);
            toast.error("Failed to update bookmark");
        }
    };

    const handleJumpPage = (e) => {
        e.preventDefault();
        const page = parseInt(jumpPage);
        if (page > 0 && page <= Math.ceil(pageInfo.count / 50)) {
            setPageInfo(prev => ({ ...prev, current: page }));
            setJumpPage('');
        } else {
            toast.error("Invalid page number");
        }
    };

    const getGradeBadgeClass = (grade) => {
        if (!grade) return 'bg-light text-dark';
        const lower = grade.toLowerCase();
        if (lower.includes('sahih')) return 'bg-success text-white';
        if (lower.includes('hasan')) return 'bg-info text-white';
        if (lower.includes('daif') || lower.includes('da\'if') || lower.includes('weak')) return 'bg-danger text-white';
        return 'bg-secondary text-white';
    };

    const totalPages = Math.ceil(pageInfo.count / 50);

    const currentBook = books.find(b => b.book_number.toString() === bookNum.toString());

    if (loading && hadiths.length === 0) {
        return (
            <div className="container-fluid d-flex justify-content-center align-items-center" style={{ minHeight: '60vh' }}>
                <div className="spinner-border text-primary" role="status"></div>
            </div>
        );
    }

    return (
        <div className="container-fluid">
            <div className="row page-titles mx-0">
                <div className="col-sm-8 p-md-0">
                    <div className="welcome-text">
                        <h4 className="mb-1">{currentBook?.english_title} - {currentBook?.arabic_title}</h4>
                        <nav aria-label="breadcrumb">
                            <ol className="breadcrumb">
                                <li className="breadcrumb-item"><Link to="/sunnah">Sunnah</Link></li>
                                <li className="breadcrumb-item"><Link to={`/sunnah/${slug}`} className="text-capitalize">{slug}</Link></li>
                                <li className="breadcrumb-item active">Book {bookNum}</li>
                            </ol>
                        </nav>
                    </div>
                </div>
                <div className="col-sm-4 p-md-0 justify-content-sm-end mt-2 mt-sm-0 d-flex align-items-center">
                    <select
                        className="form-select w-auto"
                        value={viewLanguage}
                        onChange={(e) => setViewLanguage(e.target.value)}
                    >
                        <option value="both">Both Languages</option>
                        <option value="arabic">Arabic Only</option>
                        <option value="english">English Only</option>
                    </select>
                </div>
            </div>

            <div className="row">
                {/* Left Sidebar - Book List */}
                <div className="col-xl-3 d-none d-xl-block">
                    <div className="card shadow-sm border-0 sticky-top" style={{ top: '100px', borderRadius: '1rem', maxHeight: 'calc(100vh - 120px)', overflowY: 'auto' }}>
                        <div className="card-header bg-white border-bottom py-3">
                            <h5 className="mb-0 fw-bold">Books in this Collection</h5>
                        </div>
                        <div className="list-group list-group-flush">
                            {books.map(book => (
                                <button
                                    key={book.book_number}
                                    onClick={() => navigate(`/sunnah/${slug}/book/${book.book_number}`)}
                                    className={`list-group-item list-group-item-action border-0 py-3 px-4 d-flex align-items-start ${book.book_number.toString() === bookNum.toString() ? 'active-book' : ''}`}
                                >
                                    <span className="badge rounded-pill me-3" style={{ backgroundColor: book.book_number.toString() === bookNum.toString() ? '#fff' : '#f0f0f0', color: book.book_number.toString() === bookNum.toString() ? '#1A6B4A' : '#666' }}>
                                        {book.book_number}
                                    </span>
                                    <div className="flex-grow-1">
                                        <div className="fw-bold small mb-1">{book.english_title}</div>
                                        <div className="text-end text-muted small" style={{ fontFamily: 'Amiri, serif' }}>{book.arabic_title}</div>
                                    </div>
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Main Content - Hadith Cards */}
                <div className="col-xl-9 col-lg-12">
                    {hadiths.map((hadith) => (
                        <div className="card mb-5 hadith-card shadow-sm border-0" key={hadith.id} style={{ borderRadius: '1rem' }}>
                            <div className="card-header bg-white border-0 pt-4 pb-0 d-flex justify-content-between align-items-center">
                                <div className="d-flex align-items-center gap-3">
                                    <div className="hadith-number-badge">{hadith.hadith_number}</div>
                                    {hadith.grade && (
                                        <span className={`badge rounded-pill px-3 py-2 ${getGradeBadgeClass(hadith.grade)}`}>
                                            {hadith.grade}
                                        </span>
                                    )}
                                </div>
                                <div className="d-flex gap-2">
                                    <button 
                                        className={`btn btn-icon btn-sm ${bookmarks.has(hadith.id) ? 'text-warning' : 'text-muted'}`}
                                        onClick={() => toggleBookmark(hadith.id)}
                                        title="Bookmark"
                                    >
                                        <i className={`fa${bookmarks.has(hadith.id) ? 's' : 'r'} fa-star fs-4`}></i>
                                    </button>

                                    <button className="btn btn-icon btn-sm text-muted" onClick={() => {
                                        navigator.clipboard.writeText(`${hadith.english_body}\n\n${hadith.arabic_body}`);
                                        toast.success("Copied to clipboard");
                                    }}>
                                        <i className="fa fa-copy fs-4"></i>
                                    </button>
                                </div>
                            </div>
                            
                            <div className="card-body px-4 py-4">
                                {(viewLanguage === 'arabic' || viewLanguage === 'both') && (
                                    <div className="hadith-arabic mb-4 text-end" style={{ direction: 'rtl', borderRight: '4px solid #D4AF37', paddingRight: '20px' }}>
                                        <h3
                                            className="lh-base"
                                            style={{ fontFamily: 'Amiri, serif', fontSize: '1.6rem', lineHeight: '2.4', color: '#2c3e50' }}
                                            dangerouslySetInnerHTML={{ __html: hadith.arabic_body }}
                                        />
                                    </div>
                                )}

                                {viewLanguage === 'both' && <hr className="my-4 opacity-25" />}

                                {(viewLanguage === 'english' || viewLanguage === 'both') && (
                                    <div className="hadith-english ps-2">
                                        {hadith.narrator && (
                                            <p className="fst-italic fw-bold text-dark mb-2" style={{ fontSize: '1.1rem' }}>
                                                Narrated {hadith.narrator}:
                                            </p>
                                        )}
                                        <p className="text-dark" style={{ fontSize: '1.05rem', lineHeight: '1.8' }}>
                                            {hadith.english_body}
                                        </p>
                                    </div>
                                )}
                            </div>

                            <div className="card-footer bg-light border-0 py-3 px-4 d-flex flex-wrap justify-content-between align-items-center" style={{ borderBottomLeftRadius: '1rem', borderBottomRightRadius: '1rem' }}>
                                <div className="small text-muted d-flex gap-4">
                                    <span><strong>Reference:</strong> {hadith.reference}</span>
                                    <span><strong>Hadith:</strong> {hadith.hadith_number}</span>
                                </div>
                                <div className="d-flex gap-3 mt-2 mt-sm-0">
                                    <button className="btn btn-sm btn-link text-muted p-0 text-decoration-none small">
                                        <i className="fa fa-share-alt me-1"></i> Share
                                    </button>
                                    <button className="btn btn-sm btn-link text-muted p-0 text-decoration-none small">
                                        <i className="fa fa-exclamation-triangle me-1"></i> Report
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}

                    {/* Full Pagination Footer */}
                    <div className="card shadow-sm border-0 p-4 mb-5" style={{ borderRadius: '1rem' }}>
                        <div className="row align-items-center">
                            <div className="col-md-4 mb-3 mb-md-0">
                                <span className="text-muted">Page <strong>{pageInfo.current}</strong> of <strong>{totalPages}</strong></span>
                            </div>
                            <div className="col-md-4 mb-3 mb-md-0">
                                <form onSubmit={handleJumpPage} className="d-flex justify-content-center">
                                    <div className="input-group input-group-sm w-75">
                                        <input
                                            type="number"
                                            className="form-control"
                                            placeholder="Jump to page..."
                                            value={jumpPage}
                                            onChange={(e) => setJumpPage(e.target.value)}
                                        />
                                        <button className="btn btn-outline-secondary" type="submit">Go</button>
                                    </div>
                                </form>
                            </div>
                            <div className="col-md-4 d-flex justify-content-md-end justify-content-center">
                                <nav>
                                    <ul className="pagination pagination-primary pagination-gutter mb-0">
                                        <li className={`page-item ${!pageInfo.previous ? 'disabled' : ''}`}>
                                            <button className="page-link" onClick={() => setPageInfo(p => ({...p, current: p.current - 1}))}>
                                                <i className="la la-angle-left"></i>
                                            </button>
                                        </li>

                                        {/* Simple page numbers logic */}
                                        {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                                            let pNum;
                                            if (totalPages <= 5) pNum = i + 1;
                                            else if (pageInfo.current <= 3) pNum = i + 1;
                                            else if (pageInfo.current >= totalPages - 2) pNum = totalPages - 4 + i;
                                            else pNum = pageInfo.current - 2 + i;

                                            return (
                                                <li key={pNum} className={`page-item ${pageInfo.current === pNum ? 'active' : ''}`}>
                                                    <button className="page-link" onClick={() => setPageInfo(p => ({...p, current: pNum}))}>{pNum}</button>
                                                </li>
                                            );
                                        })}

                                        <li className={`page-item ${!pageInfo.next ? 'disabled' : ''}`}>
                                            <button className="page-link" onClick={() => setPageInfo(p => ({...p, current: p.current + 1}))}>
                                                <i className="la la-angle-right"></i>
                                            </button>
                                        </li>
                                    </ul>
                                </nav>
                            </div>
                        </div>
                    </div>

                    {hadiths.length === 0 && !loading && (
                        <div className="alert alert-warning text-center rounded-3 p-5">
                            <i className="la la-frown-o fa-3x mb-3 d-block"></i>
                            <h4>No hadiths found for this book.</h4>
                            <p>Try selecting a different book or checking another collection.</p>
                            <Link to={`/sunnah/${slug}`} className="btn btn-primary mt-3">Back to Book List</Link>
                        </div>
                    )}
                </div>
            </div>

            <style dangerouslySetInnerHTML={{ __html: `
                .active-book {
                    background-color: rgba(26, 107, 74, 0.1)!important;
                    border-left: 4px solid #1A6B4A!important;
                    color: #1A6B4A!important;
                }
                .active-book .badge {
                    background-color: #1A6B4A!important;
                    color: white!important;
                }
                .hadith-number-badge {
                    background-color: #1A6B4A;
                    color: white;
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 0.9rem;
                }
                .hadith-card {
                    transition: transform 0.2s;
                }
                .hadith-card:hover {
                    transform: translateY(-3px);
                }
                .pagination-primary .page-item.active .page-link {
                    background-color: #1A6B4A!important;
                    border-color: #1A6B4A!important;
                }
                .btn-icon:hover {
                    background-color: #f8f9fa;
                }
            `}} />
        </div>
    );
};

export default HadithList;
