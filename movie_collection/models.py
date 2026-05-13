"""Module containing model definitions for movie_collection application."""
from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    """Model definition for Genre.

        Fields:
            name (CharField): required."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        """Returns string representation of Genre."""
        return self.name


class Movie(models.Model):
    """Model definition for Movie.

        Fields:
            title (CharField): required;
            description (TextField): optional;
            release_date (DateField): required;
            rating (PositiveSmallIntegerField): optional;
            genres (ManyToManyField): optional;
            owner (ForeignKey): required;
            created_at (DateTimeField): auto created date."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movies")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Returns string representation of Movie."""
        return self.title


class Review(models.Model):
    """Model definition for Review.

        Fields:
            movie (ForeignKey): required;
            owner (ForeignKey): required;
            text (TextField): required;
            rating (PositiveSmallIntegerField): required;
            created_at (DateTimeField): auto created date."""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movie_reviews")
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Returns string representation of Review."""
        return f"Review for {self.movie.title}"
