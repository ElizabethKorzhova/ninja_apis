"""This module contains schemas for ecommerce API."""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ninja import Schema


class ProductIn(Schema):
    """Represents schema for product creation."""
    name: str
    description: str = ""
    price: Decimal
    stock: int = 0


class ProductUpdate(Schema):
    """Represents schema for product update."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None


class ProductOut(Schema):
    """Represents schema for product response."""
    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    created_at: datetime


class CartItemIn(Schema):
    """Represents schema for adding product to cart."""
    product_id: int
    quantity: int = 1


class CartItemOut(Schema):
    """Represents schema for cart item response."""
    id: int
    product: ProductOut
    quantity: int
    total_price: Decimal


class CartOut(Schema):
    """Represents schema for cart response."""
    id: int
    items: list[CartItemOut]


class OrderItemOut(Schema):
    """Represents schema for order item response."""
    id: int
    product: ProductOut
    quantity: int
    price: Decimal
    total_price: Decimal


class OrderOut(Schema):
    """Represents schema for order response."""
    id: int
    status: str
    created_at: datetime
    items: list[OrderItemOut]
    total_price: Decimal


class OrderStatusUpdate(Schema):
    """Represents schema for order status update."""
    status: str
