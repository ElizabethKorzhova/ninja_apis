"""This module contains schemas for blog API."""
from datetime import datetime
from typing import Optional

from ninja import Schema


class TagIn(Schema):
    """Represents schema for tag creation."""
    name: str


class TagOut(Schema):
    """Represents schema for tag response."""
    id: int
    name: str


class PostIn(Schema):
    """Represents schema for post creation."""
    title: str
    content: str
    tag_ids: list[int] = []


class PostUpdate(Schema):
    """Represents schema for post update."""
    title: Optional[str] = None
    content: Optional[str] = None
    tag_ids: Optional[list[int]] = None


class CommentIn(Schema):
    """Represents schema for comment creation."""
    text: str


class CommentOut(Schema):
    """Represents schema for comment response."""
    id: int
    text: str
    created_at: datetime


class PostOut(Schema):
    """Represents schema for post response."""
    id: int
    title: str
    content: str
    tags: list[TagOut]
    comments: list[CommentOut]
    created_at: datetime
    updated_at: datetime
