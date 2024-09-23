import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import { Typography } from '@mui/material';
import { CheckCircle, Cancel } from '@mui/icons-material';

const API_URL = (process.env.REACT_APP_BOOKS_API_URL || 'http://localhost:8000/api/v1/books');

const BookList = ({ access_token }) => {
  const [books, setBooks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBooks = async () => {
      if (!access_token) {
        setError('No access token provided');
        setIsLoading(false);
        return;
      }

      try {
        const response = await axios.get(`${API_URL}`, {
          headers: { Authorization: `Bearer ${access_token}` }
        });
        setBooks(response.data);
        setError(null);
      } catch (error) {
        setError('Error fetching books: ' + error.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchBooks();
  }, [access_token]);

  if (!access_token) {
    return <div>Please log in to view the book list.</div>;
  }

  if (isLoading) {
    return <div>Loading books...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="booklist">
      <h2>Book List</h2>
      {books.length === 0 ? (
        <p>No books available.</p>
      ) : (
        <div className="book-grid" style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', overflowY: 'auto', maxHeight: '80vh' }}>
          {books.map((book) => (
            <div 
              key={book.id} 
              className={`book-item ${book.inventory_count > 0 ? '' : 'unavailable'}`}
              style={{
                border: '1px solid #ccc',
                borderRadius: '8px',
                padding: '10px',
                margin: '10px',
                width: '200px',
                textAlign: 'center',
                backgroundColor: book.inventory_count > 0 ? 'white' : 'lightgrey',
                opacity: book.inventory_count > 0 ? 1 : 0.5,
                transition: 'transform 0.3s, box-shadow 0.3s',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'scale(1.05)';
                e.currentTarget.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'scale(1)';
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              <img 
                src={book.image_path} 
                alt={`Cover of ${book.title}`} 
                style={{ maxWidth: '100%', height: 'auto', marginBottom: '10px' }}
              />
              <Typography variant="h6">{book.title}</Typography>
              <Typography variant="subtitle1">by {book.author}</Typography>
              <Typography variant="body1" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {book.inventory_count > 0 ? (
                  <>
                    <CheckCircle style={{ color: 'green', marginRight: '5px' }} />
                    <span style={{ fontFamily: 'Arial, sans-serif' }}>Available</span>
                  </>
                ) : (
                  <>
                    <Cancel style={{ color: 'red', marginRight: '5px' }} />
                    <span style={{ fontFamily: 'Courier New, monospace' }}>Unavailable</span>
                  </>
                )}
              </Typography>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BookList;
