"""
This module defines the database models for the books service.

It includes the Book and Transaction models, which represent the structure of the database tables.
These models use SQLAlchemy's ORM to map Python classes to database tables.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Book(Base):
    """
    Represents a book in the library system.

    Attributes:
        id (int): The unique identifier for the book.
        title (str): The title of the book.
        author (str): The author of the book.
        description (str): A description of the book.
        image_path (str): The path to the book's cover image.
        inventory_count (int): The number of copies available in the library.
        created_at (datetime): The timestamp when the book was added to the system.
        modified_at (datetime): The timestamp when the book was last modified.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(String)
    image_path = Column(String, nullable=True)
    inventory_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    transactions = relationship("Transaction", back_populates="book")

class Transaction(Base):
    """
    Represents a book rental transaction in the library system.

    Attributes:
        id (int): The unique identifier for the transaction.
        user_id (int): The ID of the user who rented the book.
        book_id (int): The ID of the book that was rented.
        rented_at (datetime): The timestamp when the book was rented.
        returned_at (datetime): The timestamp when the book was returned (nullable).
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    rented_at = Column(DateTime(timezone=True), server_default=func.now())
    returned_at = Column(DateTime(timezone=True), nullable=True)

    book = relationship("Book", back_populates="transactions")