"""This module contains schemas for movie collection API."""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from ninja import Schema


class GenreIn(Schema):
    """Represents schema for genre creation."""
    name: str


class GenreOut(Schema):
    """Represents schema for genre response."""
    id: int
    name: str


class MovieIn(Schema):
    """Represents schema for movie creation."""
    title: str
    description: str = ""
    release_date: date
    rating: Decimal = Decimal("0.0")
    genre_ids: list[int] = []


class MovieUpdate(Schema):
    """Represents schema for movie update."""
    title: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[date] = None
    rating: Optional[Decimal] = None
    genre_ids: Optional[list[int]] = None


class ReviewIn(Schema):
    """Represents schema for review creation."""
    text: str
    rating: int


class ReviewOut(Schema):
    """Represents schema for review response."""
    id: int
    text: str
    rating: int
    created_at: datetime


class MovieOut(Schema):
    """Represents schema for movie response."""
    id: int
    title: str
    description: str
    release_date: date
    rating: Decimal
    genres: list[GenreOut]
    reviews: list[ReviewOut]
    created_at: datetime
