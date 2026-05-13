"""This module contains schemas for book library API."""
from datetime import date, datetime
from typing import Optional

from ninja import Schema


class BookIn(Schema):
    """Represents schema for book creation."""
    title: str
    author: str
    genre: str
    description: str = ""
    published_date: Optional[date] = None


class BookUpdate(Schema):
    """Represents schema for book update."""
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    published_date: Optional[date] = None
    is_available: Optional[bool] = None


class BookOut(Schema):
    """Represents schema for book response."""
    id: int
    title: str
    author: str
    genre: str
    description: str
    published_date: Optional[date]
    is_available: bool
    created_at: datetime


class RentalIn(Schema):
    """Represents schema for book rental."""
    due_date: date


class RentalOut(Schema):
    """Represents schema for rental response."""
    id: int
    book: BookOut
    due_date: date
    rented_at: datetime
    returned_at: Optional[datetime]
    is_active: bool
