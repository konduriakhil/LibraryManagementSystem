"""
This module defines Pydantic models for data validation and serialization in the users service.

These schemas are used to validate incoming data and to define the structure of the API responses.
They provide a layer of type checking and data validation between the API and the database models.
"""

from pydantic import BaseModel
from .models import UserType
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """
    Base Pydantic model for User data.

    This model defines the common attributes shared by all user-related schemas.
    """
    username: str
    email: str
    user_type: UserType

class UserCreate(UserBase):
    """
    Pydantic model for creating a new user.

    This model is used when receiving data to create a new user entry.
    """
    password: str

class User(UserBase):
    """
    Pydantic model for a complete user record.

    This model is used when returning user data, including database-generated fields.
    """
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    """
    Pydantic model for token data.

    This model defines the structure of the token response.
    """
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Pydantic model for token payload data.

    This model is used for decoding and validating token data.
    """
    username: Optional[str] = None
    user_type: Optional[str] = None