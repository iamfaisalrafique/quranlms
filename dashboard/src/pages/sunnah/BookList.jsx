import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import api from '../../utils/api';
import toast from 'react-hot-toast';

const BookList = () => {
    const { slug } = useParams();
    const [books, setBooks] = useState([]);
    const [collection, setCollection] = useState(null);
    const [filteredBooks, setFilteredBooks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    // Pagination
    const [currentPage, setCurrentPage] = useState(1);
    const booksPerPage = 20;

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const [colRes, booksRes] = await Promise.all([
                    api.get(`sunnah/${slug}/`),
                    api.get(`sunnah/${slug}/books/`)
                ]);
                setCollection(colRes.data);
                setBooks(booksRes.data);
                setFilteredBooks(booksRes.data);
            } catch (error) {
                console.error("Error fetching books:", error);
                toast.error("Failed to load collection details");
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [slug]);

    useEffect(() => {
        const results = books.filter(b =>
            b.english_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            b.arabic_title.includes(searchTerm) ||
            b.book_number.toString().includes(searchTerm)
        );
        setFilteredBooks(results);
        setCurrentPage(1);
    }, [searchTerm, books]);

    // Get current books
    const indexOfLastBook = currentPage * booksPerPage;
    const indexOfFirstBook = indexOfLastBook - booksPerPage;
    const currentBooks = filteredBooks.slice(indexOfFirstBook, indexOfLastBook);
    const totalPages = Math.ceil(filteredBooks.length / booksPerPage);

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
                        <h4 className="text-capitalize">{slug.replace('-', ' ')}</h4>
                        <p className="mb-0">Browse through the books of this collection</p>
                    </div>
                </div>
                <div className="col-sm-6 p-md-0 justify-content-sm-end mt-2 mt-sm-0 d-flex">
                    <ol className="breadcrumb">
                        <li className="breadcrumb-item"><Link to="/dashboard">Dashboard</Link></li>
                        <li className="breadcrumb-item"><Link to="/sunnah">Sunnah</Link></li>
                        <li className="breadcrumb-item active"><span className="text-capitalize">{slug}</span></li>
                    </ol>
                </div>
            </div>

            {/* Collection Header Card */}
            <div className="row mb-4">
                <div className="col-12">
                    <div className="card shadow-sm border-0 overflow-hidden" style={{ borderRadius: '1rem' }}>
                        <div className="card-header bg-primary text-white border-0 py-4" style={{ backgroundColor: '#1A6B4A!important' }}>
                            <div className="w-100 text-center">
                                <h2 className="mb-2" style={{ fontFamily: 'Amiri, serif', fontSize: '2.5rem' }}>{collection?.arabic_title}</h2>
                                <h3 className="fw-bold mb-0">{collection?.english_title}</h3>
                            </div>
                        </div>
                        <div className="card-body p-4 text-center">
                            <p className="fs-5 text-dark mb-3 mx-auto" style={{ maxWidth: '800px' }}>{collection?.short_intro}</p>
                            <div className="d-flex justify-content-center gap-3">
                                <span className="badge rounded-pill px-4 py-2 fs-6" style={{ backgroundColor: '#1A6B4A', color: 'white' }}>
                                    {collection?.num_hadith} Hadiths
                                </span>
                                <span className="badge rounded-pill px-4 py-2 fs-6 bg-light text-dark border">
                                    {books.length} Books
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Search and Table */}
            <div className="row">
                <div className="col-12">
                    <div className="card shadow-sm border-0" style={{ borderRadius: '1rem' }}>
                        <div className="card-header bg-white border-bottom p-4">
                            <div className="row align-items-center">
                                <div className="col-md-6">
                                    <h4 className="card-title mb-0">List of Books</h4>
                                </div>
                                <div className="col-md-6 mt-3 mt-md-0">
                                    <div className="input-group">
                                        <span className="input-group-text bg-light border-end-0">
                                            <i className="fa fa-search text-muted"></i>
                                        </span>
                                        <input
                                            type="text"
                                            className="form-control bg-light border-start-0"
                                            placeholder="Filter books by name or number..."
                                            value={searchTerm}
                                            onChange={(e) => setSearchTerm(e.target.value)}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="card-body p-0">
                            <div className="table-responsive">
                                <table className="table table-hover mb-0">
                                    <thead className="table-light">
                                        <tr>
                                            <th className="text-center py-3" style={{ width: '100px' }}>Book #</th>
                                            <th className="py-3 text-end" style={{ width: '35%' }}>Arabic Name</th>
                                            <th className="py-3">English Name</th>
                                            <th className="text-center py-3" style={{ width: '150px' }}>Hadiths</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {currentBooks.map((book) => (
                                            <tr key={book.book_number}
                                                className="cursor-pointer transition-all"
                                                onClick={() => window.location.href=`/sunnah/${slug}/book/${book.book_number}`}
                                                style={{ cursor: 'pointer' }}
                                            >
                                                <td className="text-center align-middle fw-bold">{book.book_number}</td>
                                                <td className="text-end align-middle py-3" style={{ fontFamily: 'Amiri, serif', fontSize: '1.4rem', color: '#1A6B4A' }}>
                                                    {book.arabic_title}
                                                </td>
                                                <td className="align-middle fw-bold text-dark fs-5 py-3">
                                                    {book.english_title}
                                                </td>
                                                <td className="text-center align-middle">
                                                    <span className="badge rounded-pill light" style={{ backgroundColor: 'rgba(26, 107, 74, 0.1)', color: '#1A6B4A' }}>
                                                        {book.total_number}
                                                    </span>
                                                </td>
<<<<<<< HEAD
=======
                                                <td className="align-middle fs-5">
                                                    <Link to={`/sunnah/${slug}/book/${book.book_number}`} className="text-dark fw-medium text-decoration-none">
                                                        {book.english_title || `Book ${book.book_number}`}
                                                    </Link>
                                                </td>
                                                <td className="align-middle text-end pe-4 fs-4" style={{ fontFamily: 'Amiri, serif' }}>
                                                    {book.arabic_title}
                                                </td>
>>>>>>> origin/main
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* Pagination Footer */}
                        {totalPages > 1 && (
                            <div className="card-footer bg-white border-top p-4 d-flex justify-content-between align-items-center">
                                <span className="text-muted">
                                    Showing {indexOfFirstBook + 1} to {Math.min(indexOfLastBook, filteredBooks.length)} of {filteredBooks.length} books
                                </span>
                                <nav aria-label="Page navigation">
                                    <ul className="pagination pagination-gutter pagination-primary mb-0">
                                        <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                                            <button className="page-link" onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}>
                                                <i className="la la-angle-left"></i>
                                            </button>
                                        </li>
                                        {[...Array(totalPages)].map((_, i) => (
                                            <li key={i+1} className={`page-item ${currentPage === i + 1 ? 'active' : ''}`}>
                                                <button className="page-link" onClick={() => setCurrentPage(i + 1)}>{i + 1}</button>
                                            </li>
                                        ))}
                                        <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
                                            <button className="page-link" onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}>
                                                <i className="la la-angle-right"></i>
                                            </button>
                                        </li>
                                    </ul>
                                </nav>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            <style dangerouslySetInnerHTML={{ __html: `
                .cursor-pointer:hover {
                    background-color: rgba(26, 107, 74, 0.03)!important;
                }
                .pagination-primary .page-item.active .page-link {
                    background-color: #1A6B4A!important;
                    border-color: #1A6B4A!important;
                }
                .bg-primary {
                    background-color: #1A6B4A!important;
                }
            `}} />
        </div>
    );
};

export default BookList;
