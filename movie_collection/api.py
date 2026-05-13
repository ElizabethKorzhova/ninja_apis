"""This module contains API routes for movie_collection application."""
from datetime import date
from decimal import Decimal
from typing import Optional, List, Tuple

from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Genre, Movie, Review
from .schemas import (
    GenreIn,
    GenreOut,
    MovieIn,
    MovieOut,
    MovieUpdate,
    ReviewIn,
    ReviewOut,
)

router = Router(tags=["Movie Collection"])


@router.get("/genres/", response=List[GenreOut])
def get_genres(request: HttpRequest) -> QuerySet[Genre]:
    """Gets all genres."""
    return Genre.objects.all()


@router.post("/genres/", response={201: GenreOut})
def create_genre(request: HttpRequest, payload: GenreIn) -> Tuple[int, Genre]:
    """Creates genre."""
    genre = Genre.objects.create(**payload.dict())
    return 201, genre


@router.get("/movies/", response=List[MovieOut])
def get_movies(
    request: HttpRequest,
    genre_id: Optional[int] = None,
    min_rating: Optional[Decimal] = None,
    release_date: Optional[date] = None,
    search: Optional[str] = None,
) -> QuerySet[Movie]:
    """Gets movies with filtering and search."""
    movies = Movie.objects.prefetch_related("genres", "reviews").filter(
        owner=request.user,
    )

    if genre_id:
        movies = movies.filter(genres__id=genre_id)

    if min_rating is not None:
        movies = movies.filter(rating__gte=min_rating)

    if release_date:
        movies = movies.filter(release_date=release_date)

    if search:
        movies = movies.filter(title__icontains=search)

    return movies.distinct()


@router.get("/movies/{movie_id}", response={200: MovieOut})
def get_movie(request: HttpRequest, movie_id: int) -> Movie:
    """Gets movie by id."""
    return get_object_or_404(
        Movie.objects.prefetch_related("genres", "reviews"),
        id=movie_id,
        owner=request.user,
    )


@router.post("/movies/", response={201: MovieOut})
def create_movie(request: HttpRequest, payload: MovieIn) -> Tuple[int, Movie]:
    """Creates movie."""
    movie_data = payload.dict()
    genre_ids = movie_data.pop("genre_ids", [])

    movie = Movie.objects.create(owner=request.user, **movie_data)

    if genre_ids:
        genres = Genre.objects.filter(id__in=genre_ids)
        movie.genres.set(genres)

    return 201, movie


@router.patch("/movies/{movie_id}", response={200: MovieOut})
def update_movie(
    request: HttpRequest,
    movie_id: int,
    payload: MovieUpdate,
) -> Movie:
    """Partially updates movie."""
    movie = get_object_or_404(Movie, id=movie_id, owner=request.user)
    movie_data = payload.dict(exclude_unset=True)
    genre_ids = movie_data.pop("genre_ids", None)

    for field, value in movie_data.items():
        setattr(movie, field, value)

    movie.save()

    if genre_ids is not None:
        genres = Genre.objects.filter(id__in=genre_ids)
        movie.genres.set(genres)

    return movie


@router.delete("/movies/{movie_id}", response={204: None})
def delete_movie(request: HttpRequest, movie_id: int) -> Tuple[int, None]:
    """Deletes movie."""
    movie = get_object_or_404(Movie, id=movie_id, owner=request.user)
    movie.delete()
    return 204, None


@router.post("/movies/{movie_id}/reviews/", response={201: ReviewOut})
def create_review(
    request: HttpRequest,
    movie_id: int,
    payload: ReviewIn,
) -> Tuple[int, Review]:
    """Creates review for movie."""
    movie = get_object_or_404(Movie, id=movie_id, owner=request.user)

    review = Review.objects.create(
        movie=movie,
        owner=request.user,
        **payload.dict(),
    )

    return 201, review


@router.get("/movies/{movie_id}/reviews/", response=List[ReviewOut])
def get_movie_reviews(
    request: HttpRequest,
    movie_id: int,
) -> QuerySet[Review]:
    """Gets movie reviews."""
    movie = get_object_or_404(Movie, id=movie_id, owner=request.user)
    return movie.reviews.all()
