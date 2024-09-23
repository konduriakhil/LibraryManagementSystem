"""
This module defines the database models for the users service.

It includes the User model, which represents the structure of the users table.
The UserType enum is used to define the possible user roles in the system.
"""

from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from .database import Base
import enum

class UserType(enum.Enum):
    """
    Enum representing the possible user types in the system.
    """
    administrator = "administrator"
    librarian = "librarian"
    member = "member"

class User(Base):
    """
    Represents a user in the library system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        user_type (UserType): The type/role of the user.
        created_at (datetime): The timestamp when the user was created.
        modified_at (datetime): The timestamp when the user was last modified.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    user_type = Column(Enum(UserType))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
