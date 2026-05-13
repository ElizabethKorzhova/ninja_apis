"""This module contains API routes for book_library application."""
from typing import List, Optional, Tuple

from django.db.models import Q, QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone as django_timezone
from ninja import Router

from .models import Book, Rental
from .schemas import BookIn, BookOut, BookUpdate, RentalIn, RentalOut

router = Router(tags=["Book Library"])


@router.get("/books/", response=List[BookOut])
def get_books(
    request: HttpRequest,
    search: Optional[str] = None,
) -> QuerySet[Book]:
    """Gets books with search by title, author or genre."""
    books = Book.objects.all()
    if search:
        books = books.filter(
            Q(title__icontains=search)
            | Q(author__icontains=search)
            | Q(genre__icontains=search)
        )
    return books.order_by("-created_at")


@router.get("/books/{book_id}", response={200: BookOut})
def get_book(request: HttpRequest, book_id: int) -> Book:
    """Gets one book by id."""
    return get_object_or_404(Book, id=book_id)


@router.post("/books/", response={201: BookOut})
def create_book(request: HttpRequest, payload: BookIn) -> Tuple[int, Book]:
    """Creates a new book."""
    book = Book.objects.create(owner=request.user, **payload.dict())
    return 201, book


@router.patch("/books/{book_id}", response={200: BookOut})
def update_book(
    request: HttpRequest,
    book_id: int,
    payload: BookUpdate,
) -> Book:
    """Partially updates book by id."""
    book = get_object_or_404(Book, id=book_id, owner=request.user)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(book, field, value)

    book.save()
    return book


@router.delete("/books/{book_id}", response={204: None})
def delete_book(request: HttpRequest, book_id: int) -> Tuple[int, None]:
    """Deletes book by id."""
    book = get_object_or_404(Book, id=book_id, owner=request.user)
    book.delete()
    return 204, None


@router.post("/books/{book_id}/rent/", response={201: RentalOut})
def rent_book(
    request: HttpRequest,
    book_id: int,
    payload: RentalIn,
) -> Tuple[int, Rental]:
    """Rents a book for authenticated user."""
    book = get_object_or_404(Book, id=book_id)

    if not book.is_available:
        raise ValueError("Book is not available.")

    rental = Rental.objects.create(book=book, user=request.user, due_date=payload.due_date)
    book.is_available = False
    book.save()
    return 201, rental


@router.get("/rentals/", response=List[RentalOut])
def get_rentals(request: HttpRequest, active_only: bool = False) -> QuerySet[Rental]:
    """Gets authenticated user's rentals."""
    rentals = Rental.objects.select_related("book").filter(user=request.user)
    if active_only:
        rentals = rentals.filter(returned_at__isnull=True)
    return rentals.order_by("-rented_at")


@router.post("/rentals/{rental_id}/return/", response={200: RentalOut})
def return_rental(request: HttpRequest, rental_id: int) -> Rental:
    """Returns rented book."""
    rental = get_object_or_404(
        Rental.objects.select_related("book"),
        id=rental_id,
        user=request.user,
    )

    if rental.returned_at is None:
        rental.returned_at = django_timezone.now()
        rental.save()
        rental.book.is_available = True
        rental.book.save()

    return rental
