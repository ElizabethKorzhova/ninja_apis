"""This module contains schemas for task manager API."""
from datetime import date, datetime
from typing import Optional

from ninja import Schema


class TaskIn(Schema):
    """Represents schema for task creation."""
    title: str
    description: str = ""
    status: str = "not_done"
    due_date: Optional[date] = None


class TaskUpdate(Schema):
    """Represents schema for partial task update."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[date] = None


class TaskOut(Schema):
    """Represents schema for task response."""
    id: int
    title: str
    description: str
    status: str
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime
