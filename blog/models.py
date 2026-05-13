"""Module containing model definitions for blog application."""
from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    """Model definition for Tag.

        Fields:
            name (CharField): required;"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        """Returns string representation of Tag."""
        return self.name


class Post(models.Model):
    """Model definition for Post.

        Fields:
            title (CharField): required;
            content (TextField): required;
            author (ForeignKey): required;
            tags (ManyToManyField): optional;
            created_at (DateTimeField): auto created date;
            updated_at (DateTimeField): auto created date."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Returns string representation of Post."""
        return self.title


class Comment(models.Model):
    """Model definition for Comment.

        Fields:
            post (ForeignKey): required;
            author (ForeignKey): required;
            text (TextField): required;
            created_at (DateTimeField): auto created date."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Returns string representation of Comment."""
        return f"Comment by {self.author.username}"
