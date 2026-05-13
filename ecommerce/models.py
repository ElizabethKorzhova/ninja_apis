"""Module containing model definitions for ecommerce application."""

from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    """Model definition for Product.

        Fields:
            name (CharField): required;
            description (TextField): not required;
            price (DecimalField): required;
            stock (PositiveIntegerField): required;
            created_at (DateTimeField): auto created date."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Returns string representation of Product."""
        return self.name


class Cart(models.Model):
    """Model definition for Cart.

        Fields:
            owner (OneToOneField): required;
            created_at (DateTimeField): auto created date."""
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Returns string representation of Cart."""
        return f"Cart of {self.owner.username}"


class CartItem(models.Model):
    """Model definition for CartItem.

        Fields:
            cart (ForeignKey): required;
            product (ForeignKey): required;
            quantity (PositiveIntegerField): required."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        """Meta definition for CartItem."""
        unique_together = ("cart", "product")

    def __str__(self) -> str:
        """Returns string representation of CartItem."""
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self) -> Decimal:
        """Calculates total price for CartItem."""
        return self.product.price * self.quantity


class Order(models.Model):
    """Model definition for Order.

        Fields:
            owner (ForeignKey): required;
            status (CharField): required;
            created_at (DateTimeField): auto created date."""
    STATUS_CHOICES = [
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="processing")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Returns string representation of Order."""
        return f"Order #{self.id} by {self.owner.username}"

    @property
    def total_price(self) -> Decimal:
        """Calculates total order price."""
        return sum((item.total_price for item in self.items.all()), Decimal("0"))


class OrderItem(models.Model):
    """Model definition for OrderItem.

        Fields:
            order (ForeignKey): required;
            product (ForeignKey): required;
            quantity (PositiveIntegerField): required;
            price (DecimalField): required;"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        """Returns string representation of OrderItem."""
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self) -> Decimal:
        """Calculates total price for order item."""
        return self.price * self.quantity
