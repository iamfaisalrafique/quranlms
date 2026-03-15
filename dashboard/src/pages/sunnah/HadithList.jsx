import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import api from '../../utils/api';
import toast from 'react-hot-toast';

const HadithList = () => {
    const { slug, bookNum } = useParams();
    const [hadiths, setHadiths] = useState([]);
    const [loading, setLoading] = useState(true);
    const [pageUrl, setPageUrl] = useState(`sunnah/collection/${slug}/book/${bookNum}/hadiths/`);
    const [nextUrl, setNextUrl] = useState(null);
    const [prevUrl, setPrevUrl] = useState(null);
    const [bookData, setBookData] = useState(null);
    const [bookmarks, setBookmarks] = useState(new Set());

    useEffect(() => {
        const fetchHadiths = async () => {
            setLoading(true);
            try {
                // Determine if we are fetching by relative or absolute URL (from DRF pagination)
                const url = pageUrl.startsWith('http') ? pageUrl : pageUrl;
                
                const [hadithRes, bookmarksRes] = await Promise.all([
                    api.get(url),
                    api.get('sunnah/bookmarks/')
                ]);

                // DRF Paginated Response
                if (hadithRes.data.results) {
                    setHadiths(hadithRes.data.results);
                    setNextUrl(hadithRes.data.next);
                    setPrevUrl(hadithRes.data.previous);
                } else {
                    setHadiths(hadithRes.data);
                }

                if (hadithRes.data.results && hadithRes.data.results.length > 0) {
                    setBookData(hadithRes.data.results[0].book);
                }
                
                // Set bookmarks by hadith ID
                const bms = new Set(bookmarksRes.data.map(b => b.hadith));
                setBookmarks(bms);
            } catch (error) {
                console.error("Error fetching hadiths:", error);
                toast.error("Failed to load hadiths");
            } finally {
                setLoading(false);
            }
        };

        fetchHadiths();
    }, [pageUrl]);

    const toggleBookmark = async (hadithId) => {
        try {
            if (bookmarks.has(hadithId)) {
                // Find bookmark ID - unfortunately we don't have the bookmark ID mapped easily 
                // Let's refetch bookmarks to get the specific ID to delete
                const res = await api.get('sunnah/bookmarks/');
                const bm = res.data.find(b => b.hadith === hadithId);
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
                await api.post('sunnah/bookmark/', { hadith: hadithId });
                setBookmarks(prev => new Set([...prev, hadithId]));
                toast.success("Bookmark added");
            }
        } catch (error) {
            console.error(error);
            toast.error("Failed to update bookmark");
        }
    };

    const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text);
        toast.success("Copied to clipboard!");
    };

    const getGradeBadgeClass = (grade) => {
        if (!grade) return 'badge-light text-dark';
        const lower = grade.toLowerCase();
        if (lower.includes('sahih')) return 'badge-success';
        if (lower.includes('hasan')) return 'badge-info';
        if (lower.includes('daif') || lower.includes('da\'if') || lower.includes('weak')) return 'badge-danger';
        if (lower.includes('maqtu') || lower.includes('mursal')) return 'badge-warning';
        return 'badge-secondary';
    };

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
                <div className="col-sm-6 p-md-0">
                    <div className="welcome-text">
                        <h4>{bookData ? bookData.name_en : `Book ${bookNum}`}</h4>
                        <p className="mb-0 text-capitalize">{slug}</p>
                    </div>
                </div>
                <div className="col-sm-6 p-md-0 justify-content-sm-end mt-2 mt-sm-0 d-flex">
                    <ol className="breadcrumb">
                        <li className="breadcrumb-item"><Link to="/dashboard">Dashboard</Link></li>
                        <li className="breadcrumb-item"><Link to="/sunnah">Sunnah</Link></li>
                        <li className="breadcrumb-item"><Link to={`/sunnah/${slug}`} className="text-capitalize">{slug}</Link></li>
                        <li className="breadcrumb-item active">Book {bookNum}</li>
                    </ol>
                </div>
            </div>

            <div className="row justify-content-center">
                <div className="col-xl-9 col-lg-12">
                    {/* Pagination Controls Top */}
                    <div className="d-flex justify-content-between mb-4">
                        <button 
                            className="btn btn-primary" 
                            disabled={!prevUrl} 
                            onClick={() => setPageUrl(prevUrl)}
                        >
                            <i className="fa fa-arrow-left me-2"></i> Previous
                        </button>
                        <button 
                            className="btn btn-primary" 
                            disabled={!nextUrl} 
                            onClick={() => setPageUrl(nextUrl)}
                        >
                            Next <i className="fa fa-arrow-right ms-2"></i>
                        </button>
                    </div>

                    {hadiths.map((hadith) => (
                        <div className="card mb-4 shadow-sm" key={hadith.id}>
                            <div className="card-header bg-light d-flex justify-content-between align-items-center py-2">
                                <h5 className="mb-0 text-primary fw-bold">
                                    <i className="la la-book me-2"></i>
                                    Hadith {hadith.hadith_number}
                                </h5>
                                
                                <div className="d-flex gap-2">
                                    <button 
                                        className={`btn btn-sm ${bookmarks.has(hadith.id) ? 'btn-primary' : 'btn-outline-primary'}`}
                                        onClick={() => toggleBookmark(hadith.id)}
                                        title="Bookmark"
                                    >
                                        <i className="fa fa-bookmark"></i>
                                    </button>
                                    <button 
                                        className="btn btn-sm btn-outline-secondary"
                                        onClick={() => copyToClipboard(`${hadith.body_en}\n\n${hadith.body_ar}`)}
                                        title="Copy Hadith"
                                    >
                                        <i className="fa fa-copy"></i>
                                    </button>
                                </div>
                            </div>
                            
                            <div className="card-body">
                                {/* Grade Badge */}
                                {hadith.grade && (
                                    <div className="mb-4 text-center">
                                        <span className={`badge ${getGradeBadgeClass(hadith.grade)} fs-6 py-2 px-3`}>
                                            <strong>Grade:</strong> {hadith.grade}
                                        </span>
                                    </div>
                                )}

                                {/* Arabic Text (Right Aligned, Amish Font) */}
                                <div className="mb-5 text-end" style={{ direction: 'rtl' }}>
                                    <h3 
                                        className="text-dark lh-base" 
                                        style={{ fontFamily: 'Amiri, serif', fontSize: '1.8rem', lineHeight: '2.4' }}
                                        dangerouslySetInnerHTML={{ __html: hadith.body_ar }}
                                    />
                                </div>

                                <hr className="my-4" />

                                {/* English Text */}
                                <div>
                                    {hadith.narrator_en && (
                                        <p className="fw-bold text-dark fs-5 mb-2">Narrated {hadith.narrator_en}:</p>
                                    )}
                                    <p 
                                        className="text-dark fs-5" 
                                        style={{ lineHeight: '1.8' }}
                                        dangerouslySetInnerHTML={{ __html: hadith.body_en }}
                                    />
                                </div>
                            </div>
                            
                            <div className="card-footer bg-light py-2 text-muted fs-6">
                                <div className="row text-center mb-0">
                                    <div className="col-4 border-end">
                                        <strong>Ref:</strong> {hadith.reference || `Book ${bookNum}, Hadith ${hadith.hadith_number}`}
                                    </div>
                                    <div className="col-4 border-end">
                                        <strong>In-book:</strong> {hadith.in_book_reference || hadith.hadith_number}
                                    </div>
                                    <div className="col-4 text-capitalize">
                                        <strong>Collection:</strong> {slug.replace('-', ' ')}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}

                    {/* Pagination Controls Bottom */}
                    <div className="d-flex justify-content-between mt-4 mb-5">
                        <button 
                            className="btn btn-primary" 
                            disabled={!prevUrl} 
                            onClick={() => setPageUrl(prevUrl)}
                        >
                            <i className="fa fa-arrow-left me-2"></i> Previous
                        </button>
                        <button 
                            className="btn btn-primary" 
                            disabled={!nextUrl} 
                            onClick={() => setPageUrl(nextUrl)}
                        >
                            Next <i className="fa fa-arrow-right ms-2"></i>
                        </button>
                    </div>

                    {hadiths.length === 0 && !loading && (
                        <div className="alert alert-warning text-center">
                            No hadiths found for this book.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default HadithList;
