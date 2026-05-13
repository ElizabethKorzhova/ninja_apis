"""This module contains schemas for server monitoring API."""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from ninja import Schema


class ServerIn(Schema):
    """Represents schema for server creation."""
    name: str
    host: str
    status: str = "online"


class ServerUpdate(Schema):
    """Represents schema for server update."""
    name: Optional[str] = None
    host: Optional[str] = None
    status: Optional[str] = None


class AlertOut(Schema):
    """Represents schema for alert response."""
    id: int
    message: str
    created_at: datetime


class ServerMetricIn(Schema):
    """Represents schema for server metric creation."""
    cpu_usage: Decimal
    memory_usage: Decimal
    load_average: Decimal


class ServerMetricOut(Schema):
    """Represents schema for server metric response."""
    id: int
    cpu_usage: Decimal
    memory_usage: Decimal
    load_average: Decimal
    recorded_at: datetime
    is_critical: bool


class ServerOut(Schema):
    """Represents schema for server response."""
    id: int
    name: str
    host: str
    status: str
    created_at: datetime
    updated_at: datetime


class ServerDetailsOut(ServerOut):
    """Represents schema for detailed server response."""
    metrics: List[ServerMetricOut]
    alerts: List[AlertOut]
