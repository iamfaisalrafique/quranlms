import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import api from '../../utils/api';
import toast from 'react-hot-toast';

const BookList = () => {
    const { slug } = useParams();
    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchBooks = async () => {
            try {
                const response = await api.get(`sunnah/collection/${slug}/books/`);
                setBooks(response.data);
                setLoading(false);
            } catch (error) {
                console.error("Error fetching books:", error);
                toast.error("Failed to load books for this collection");
                setLoading(false);
            }
        };

        fetchBooks();
    }, [slug]);

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
                        <p className="mb-0">Browse books in this collection</p>
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

            <div className="row">
                <div className="col-12">
                    <div className="card">
                        <div className="card-header bg-primary">
                            <h4 className="card-title text-white">Books</h4>
                        </div>
                        <div className="card-body p-0">
                            <div className="table-responsive">
                                <table className="table table-hover table-striped mb-0">
                                    <thead className="thead-light">
                                        <tr>
                                            <th className="text-center" style={{ width: '80px' }}>Book</th>
                                            <th>English Title</th>
                                            <th className="text-end pe-4">Arabic Title</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {books.map((book) => (
                                            <tr key={book.id} style={{ cursor: 'pointer' }} onClick={() => window.location.href=`/sunnah/${slug}/book/${book.book_number}`}>
                                                <td className="text-center align-middle">
                                                    <span className="badge badge-primary light badge-rounded px-3 py-2 fs-5">
                                                        {book.book_number}
                                                    </span>
                                                </td>
                                                <td className="align-middle fs-5">
                                                    <Link to={`/sunnah/${slug}/book/${book.book_number}`} className="text-dark fw-medium text-decoration-none">
                                                        {book.name_en || `Book ${book.book_number}`}
                                                    </Link>
                                                </td>
                                                <td className="align-middle text-end pe-4 fs-4" style={{ fontFamily: 'Amiri, serif' }}>
                                                    {book.name_ar}
                                                </td>
                                            </tr>
                                        ))}
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

export default BookList;
