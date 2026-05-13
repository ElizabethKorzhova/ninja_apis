"""This module contains main API configuration."""
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from ninja import NinjaAPI
from ninja.security import django_auth

from task_manager.api import router as task_router
from ecommerce.api import router as ecommerce_router
from movie_collection.api import router as movie_collection_router
from blog.api import router as blog_router

api = NinjaAPI(
    title="Django Ninja API",
    version="1.0.0",
    auth=django_auth,
)

@api.get("/csrf/", auth=None)
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request: HttpRequest) -> JsonResponse:
    """Sets CSRF cookie for Swagger."""
    return JsonResponse({"detail": "CSRF cookie set"})


api.add_router("/tasks/", task_router)
api.add_router("/ecommerce/", ecommerce_router)
api.add_router("/movies/", movie_collection_router)
api.add_router("/blogs/", blog_router)
