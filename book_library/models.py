"""Module containing model definitions for book_library application."""
from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    """Model definition for Book.

        Fields:
            title (CharField): required;
            author (CharField): not required;
            genre (CharField): required;
            description (TextField): optional;
            published_date (DateField): optional;
            is_available (BooleanField): required;
            owner (ForeignKey): required;
            created_at (DateTimeField): auto created date."""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Returns string representation of Book."""
        return self.title


class Rental(models.Model):
    """Model definition for Rental.

        Fields:
            book (ForeignKey): required;
            user (ForeignKey): required;
            due_date (DateField): required;
            rented_at (DateTimeField): auto created date;
            returned_at (DateTimeField): optional."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="rentals")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rentals")
    due_date = models.DateField()
    rented_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        """Returns string representation of Rental."""
        return f"{self.book.title} rented by {self.user.username}"

    @property
    def is_active(self) -> bool:
        """Checks whether rental is active."""
        return self.returned_at is None
