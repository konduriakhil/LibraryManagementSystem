import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Books() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_BOOKS_API_URL}/books/`);
        setBooks(response.data);
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    };

    fetchBooks();
  }, []);

  return (
    <div>
      <h1>Books</h1>
      <ul>
        {books.map((book) => (
          <li key={book.id}>
            <h3>{book.title}</h3>
            <p>Author: {book.author}</p>
            <p>Description: {book.description}</p>
            {book.image_path && (
              <img 
                src={`${process.env.REACT_APP_BOOKS_API_URL}${book.image_path}`} 
                alt={`Cover of ${book.title}`} 
                style={{ maxWidth: '200px', height: 'auto' }}
              />
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Books;