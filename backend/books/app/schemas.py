"""
This module defines Pydantic models for data validation and serialization in the books service.

These schemas are used to validate incoming data and to define the structure of the API responses.
They provide a layer of type checking and data validation between the API and the database models.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    """
    Base Pydantic model for Book data.

    This model defines the common attributes shared by all book-related schemas.
    """
    title: str
    author: str
    description: str
    image_path: Optional[str] = None
    inventory_count: int

class BookCreate(BookBase):
    """
    Pydantic model for creating a new book.

    This model is used when receiving data to create a new book entry.
    """
    pass

class Book(BookBase):
    """
    Pydantic model for a complete book record.

    This model is used when returning book data, including database-generated fields.
    """
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    """
    Base Pydantic model for Transaction data.

    This model defines the common attributes shared by all transaction-related schemas.
    """
    user_id: int
    book_id: int

class TransactionCreate(TransactionBase):
    """
    Pydantic model for creating a new transaction.

    This model is used when receiving data to create a new transaction entry.
    """
    pass

class Transaction(TransactionBase):
    """
    Pydantic model for a complete transaction record.

    This model is used when returning transaction data, including database-generated fields.
    """
    id: int
    rented_at: datetime
    returned_at: Optional[datetime]

    class Config:
        orm_mode = True