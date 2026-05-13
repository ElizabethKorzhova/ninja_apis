"""Module containing model definitions for task_manager application."""
from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    """Model definition for TaskComment.

        Fields:
            title (CharField): required;
            description (TextField): not required;
            status (CharField): required;
            due_date (DateField): not required;
            created_at (DateTimeField): auto created date;
            updated_at (DateTimeField): auto updated date;
            owner (ForeignKey): required;"""
    STATUS_CHOICES = [
        ("not_done", "Not done"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self) -> str:
        """Returns string representation of Task."""
        return self.title
