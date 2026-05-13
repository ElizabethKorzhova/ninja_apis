"""This module contains API routes for ecommerce application."""
from typing import List, Tuple

from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Cart, CartItem, Order, OrderItem, Product
from .schemas import (
    CartItemIn,
    CartOut,
    OrderOut,
    OrderStatusUpdate,
    ProductIn,
    ProductOut,
    ProductUpdate,
)

router = Router(tags=["E-commerce"])


@router.get("/products/", response=List[ProductOut])
def get_products(request: HttpRequest) -> QuerySet[Product]:
    """Gets all products."""
    return Product.objects.all()


@router.get("/products/{product_id}", response={200: ProductOut})
def get_product(request: HttpRequest, product_id: int) -> Product:
    """Gets product by id."""
    return get_object_or_404(Product, id=product_id)


@router.post("/products/", response={201: ProductOut})
def create_product(request: HttpRequest, payload: ProductIn) -> Tuple[int, Product]:
    """Creates product."""
    product = Product.objects.create(**payload.dict())
    return 201, product


@router.patch("/products/{product_id}", response={200: ProductOut})
def update_product(
    request: HttpRequest,
    product_id: int,
    payload: ProductUpdate,
) -> Product:
    """Partially updates product."""
    product = get_object_or_404(Product, id=product_id)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(product, field, value)

    product.save()
    return product


@router.delete("/products/{product_id}", response={204: None})
def delete_product(request: HttpRequest, product_id: int) -> Tuple[int, None]:
    """Deletes product."""
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return 204, None


@router.get("/cart/", response=CartOut)
def get_cart(request: HttpRequest) -> Cart:
    """Gets user's cart."""
    cart, _ = Cart.objects.get_or_create(owner=request.user)
    return cart


@router.post("/cart/items/", response={201: CartOut})
def add_product_to_cart(
    request: HttpRequest,
    payload: CartItemIn,
) -> Tuple[int, Cart]:
    """Adds product to user's cart."""
    cart, _ = Cart.objects.get_or_create(owner=request.user)
    product = get_object_or_404(Product, id=payload.product_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": payload.quantity},
    )

    if not created:
        cart_item.quantity += payload.quantity
        cart_item.save()

    return 201, cart


@router.delete("/cart/items/{item_id}", response={204: None})
def remove_product_from_cart(
    request: HttpRequest,
    item_id: int,
) -> Tuple[int, None]:
    """Removes product from authenticated user's cart."""
    cart, _ = Cart.objects.get_or_create(owner=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    cart_item.delete()
    return 204, None


@router.post("/orders/", response={201: OrderOut})
@transaction.atomic
def create_order(request: HttpRequest) -> tuple[int, Order]:
    """Creates order from authenticated user's cart."""
    cart, _ = Cart.objects.get_or_create(owner=request.user)
    cart_items = cart.items.select_related("product")

    if not cart_items.exists():
        raise ValueError("Cart is empty.")

    order = Order.objects.create(owner=request.user)

    for cart_item in cart_items:
        product = cart_item.product

        if product.stock < cart_item.quantity:
            raise ValueError(f"Not enough stock for {product.name}.")

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=cart_item.quantity,
            price=product.price,
        )

        product.stock -= cart_item.quantity
        product.save()

    cart_items.delete()
    return 201, order


@router.get("/orders/", response=list[OrderOut])
def get_orders(request: HttpRequest) -> QuerySet[Order]:
    """Gets authenticated user's orders."""
    return Order.objects.filter(owner=request.user)


@router.get("/orders/{order_id}", response={200: OrderOut})
def get_order(request: HttpRequest, order_id: int) -> Order:
    """Gets authenticated user's order by id."""
    return get_object_or_404(Order, id=order_id, owner=request.user)


@router.patch("/orders/{order_id}/status/", response={200: OrderOut})
def update_order_status(
    request: HttpRequest,
    order_id: int,
    payload: OrderStatusUpdate,
) -> Order:
    """Updates order status."""
    order = get_object_or_404(Order, id=order_id, owner=request.user)
    order.status = payload.status
    order.save()
    return order
