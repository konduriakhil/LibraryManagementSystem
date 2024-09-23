import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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
        const response = await axios.get(`${API_URL}/api/v1/books`, {
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
        <Carousel showArrows={true} infiniteLoop={true} showThumbs={false}>
          {books.map((book) => (
            <div 
              key={book.id} 
              className="book-slide"
              style={{
                backgroundImage: `url(${book.image_path})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                height: '400px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-end',
                padding: '20px',
                color: 'white',
                textShadow: '2px 2px 4px rgba(0,0,0,0.7)'
              }}
            >
              <h3>{book.title}</h3>
              <p>by {book.author}</p>
            </div>
          ))}
        </Carousel>
      )}
    </div>
  );
};

export default BookList;
