"""
This module is the main entry point for the books service API.

It defines the FastAPI application and all the API endpoints for managing books and transactions.
The module includes authentication and authorization checks for protected routes.
"""

from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from datetime import datetime
import jwt
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Define the allowed origins
origins = [
    "http://localhost:3000",  # Add the frontend URL you want to allow
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verifies the JWT token provided in the request.

    Args:
        credentials (HTTPAuthorizationCredentials): The credentials containing the JWT token.

    Returns:
        dict: The decoded payload of the JWT token.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def is_authenticated(func):
    """
    Decorator to check if the user is authenticated.

    This decorator verifies the JWT token and adds the user payload to the function kwargs.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        credentials = kwargs.get('credentials')
        if not credentials:
            raise HTTPException(status_code=401, detail="Authentication credentials missing")
        verify_token(credentials)
        #kwargs['user_payload'] = payload
        return await func(*args, **kwargs)
    return wrapper

def is_admin_or_librarian(func):
    """
    Decorator to check if the user is an administrator or librarian.

    This decorator checks the user type in the JWT payload and allows access only to
    administrators and librarians.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user_payload = kwargs.get('user_payload')
        if not user_payload:
            raise HTTPException(status_code=401, detail="Authentication required")
        user_type = user_payload.get("user_type")
        if user_type not in ["administrator", "librarian"]:
            raise HTTPException(status_code=403, detail="Not authorized")
        return await func(*args, **kwargs)
    return wrapper

@app.post("/api/v1/books/", response_model=schemas.Book)
@is_authenticated
@is_admin_or_librarian
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Create a new book entry.

    This endpoint is protected and only accessible to administrators and librarians.

    Args:
        book (schemas.BookCreate): The book data to be created.
        db (Session): The database session.
        credentials (HTTPAuthorizationCredentials): The authentication credentials.

    Returns:
        schemas.Book: The created book entry.
    """
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/api/v1/books/", response_model=list[schemas.Book])
@is_authenticated
async def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Retrieve a list of books.

    This endpoint is protected and accessible to all authenticated users.

    Args:
        skip (int): The number of books to skip (for pagination).
        limit (int): The maximum number of books to return.
        db (Session): The database session.
        credentials (HTTPAuthorizationCredentials): The authentication credentials.

    Returns:
        list[schemas.Book]: A list of book entries.
    """
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

@app.get("/api/v1/books/{book_id}", response_model=schemas.Book)
@is_authenticated
async def read_book(book_id: int, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Retrieve a specific book by ID.

    This endpoint is protected and accessible to all authenticated users.

    Args:
        book_id (int): The ID of the book to retrieve.
        db (Session): The database session.
        credentials (HTTPAuthorizationCredentials): The authentication credentials.

    Returns:
        schemas.Book: The book entry.

    Raises:
        HTTPException: If the book is not found.
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/api/v1/books/{book_id}", response_model=schemas.Book)
@is_authenticated
@is_admin_or_librarian
async def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Update a book entry.

    This endpoint is protected and only accessible to administrators and librarians.

    Args:
        book_id (int): The ID of the book to update.
        book (schemas.BookCreate): The updated book data.
        db (Session): The database session.
        credentials (HTTPAuthorizationCredentials): The authentication credentials.

    Returns:
        schemas.Book: The updated book entry.

    Raises:
        HTTPException: If the book is not found.
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/api/v1/books/{book_id}", response_model=schemas.Book)
@is_authenticated
@is_admin_or_librarian
async def delete_book(book_id: int, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Delete a book entry.

    This endpoint is protected and only accessible to administrators and librarians.

    Args:
        book_id (int): The ID of the book to delete.
        db (Session): The database session.
        credentials (HTTPAuthorizationCredentials): The authentication credentials.

    Returns:
        schemas.Book: The deleted book entry.

    Raises:
        HTTPException: If the book is not found.
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book

@app.post("/api/v1/transactions/rent", response_model=schemas.Transaction)
@is_authenticated
async def rent_book(transaction: schemas.TransactionCreate, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Rent a book.

    This endpoint is protected and accessible to all authenticated users.

    Args:
        transaction (schemas.TransactionCreate): The transaction data.
        db (Session): The database session.
        credentials (HTTPAuthorizationCredentials): The authentication credentials.

    Returns:
        schemas.Transaction: The created transaction entry.

    Raises:
        HTTPException: If the book is not found or not available for rent.
    """
    db_book = db.query(models.Book).filter(models.Book.id == transaction.book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.inventory_count <= 0:
        raise HTTPException(status_code=400, detail="Book is not available for rent")
    
    db_transaction = models.Transaction(**transaction.dict())
    db_book.inventory_count -= 1
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.put("/api/v1/transactions/{transaction_id}/return", response_model=schemas.Transaction)
@is_authenticated
async def return_book(transaction_id: int, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Return a rented book.

    This endpoint is protected and accessible to all authenticated users.

    Args:
        transaction_id (int): The ID of the transaction to update.
        db (Session): The database session.
        credentials (HTTPAuthorizationCredentials): The authentication credentials.

    Returns:
        schemas.Transaction: The updated transaction entry.

    Raises:
        HTTPException: If the transaction is not found or the book has already been returned.
    """
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if db_transaction.returned_at is not None:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    db_transaction.returned_at = datetime.utcnow()
    db_book = db.query(models.Book).filter(models.Book.id == db_transaction.book_id).first()
    db_book.inventory_count += 1
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/api/v1/transactions/", response_model=list[schemas.Transaction])
@is_authenticated
@is_admin_or_librarian
async def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Retrieve a list of transactions.

    This endpoint is protected and only accessible to administrators and librarians.

    Args:
        skip (int): The number of transactions to skip (for pagination).
        limit (int): The maximum number of transactions to return.
        db (Session): The database session.
        credentials (HTTPAuthorizationCredentials): The authentication credentials.

    Returns:
        list[schemas.Transaction]: A list of transaction entries.
    """
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions

@app.get("/api/v1/transactions/{transaction_id}", response_model=schemas.Transaction)
@is_authenticated
async def read_transaction(transaction_id: int, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Retrieve a specific transaction by ID.

    This endpoint is protected and accessible to all authenticated users.

    Args:
        transaction_id (int): The ID of the transaction to retrieve.
        db (Session): The database session.
        credentials (HTTPAuthorizationCredentials): The authentication credentials.

    Returns:
        schemas.Transaction: The transaction entry.

    Raises:
        HTTPException: If the transaction is not found.
    """
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction