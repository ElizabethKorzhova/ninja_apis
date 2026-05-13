"""This module contains API routes for blog application."""
from typing import Tuple, List

from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Comment, Post, Tag
from .schemas import (
    CommentIn,
    CommentOut,
    PostIn,
    PostOut,
    PostUpdate,
    TagIn,
    TagOut,
)

router = Router(tags=["Blog Platform"])


@router.get("/tags/", response=List[TagOut])
def get_tags(request: HttpRequest) -> QuerySet[Tag]:
    """Gets all tags."""
    return Tag.objects.all()


@router.post("/tags/", response={201: TagOut})
def create_tag(request: HttpRequest, payload: TagIn) -> Tuple[int, Tag]:
    """Creates tag."""
    tag = Tag.objects.create(**payload.dict())
    return 201, tag


@router.get("/posts/", response=List[PostOut])
def get_posts(request: HttpRequest) -> QuerySet[Post]:
    """Gets user's posts."""
    return Post.objects.prefetch_related("tags", "comments").filter(
        author=request.user,
    )


@router.get("/posts/{post_id}", response={200: PostOut})
def get_post(request: HttpRequest, post_id: int) -> Post:
    """Gets post by id."""
    return get_object_or_404(
        Post.objects.prefetch_related("tags", "comments"),
        id=post_id,
        author=request.user,
    )


@router.post("/posts/", response={201: PostOut})
def create_post(request: HttpRequest, payload: PostIn) -> Tuple[int, Post]:
    """Creates post."""
    post_data = payload.dict()
    tag_ids = post_data.pop("tag_ids", [])

    post = Post.objects.create(author=request.user, **post_data)

    if tag_ids:
        tags = Tag.objects.filter(id__in=tag_ids)
        post.tags.set(tags)

    return 201, post


@router.patch("/posts/{post_id}", response={200: PostOut})
def update_post(
    request: HttpRequest,
    post_id: int,
    payload: PostUpdate,
) -> Post:
    """Partially updates post."""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post_data = payload.dict(exclude_unset=True)
    tag_ids = post_data.pop("tag_ids", None)

    for field, value in post_data.items():
        setattr(post, field, value)

    post.save()

    if tag_ids is not None:
        tags = Tag.objects.filter(id__in=tag_ids)
        post.tags.set(tags)

    return post


@router.delete("/posts/{post_id}", response={204: None})
def delete_post(request: HttpRequest, post_id: int) -> Tuple[int, None]:
    """Deletes post."""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return 204, None


@router.post("/posts/{post_id}/comments/", response={201: CommentOut})
def create_comment(
    request: HttpRequest,
    post_id: int,
    payload: CommentIn,
) -> Tuple[int, Comment]:
    """Creates comment for post."""
    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(
        post=post,
        author=request.user,
        **payload.dict(),
    )
    return 201, comment


@router.get("/posts/{post_id}/comments/", response=List[CommentOut])
def get_comments(
    request: HttpRequest,
    post_id: int,
) -> QuerySet[Comment]:
    """Gets post comments."""
    post = get_object_or_404(Post, id=post_id)
    return post.comments.all()
