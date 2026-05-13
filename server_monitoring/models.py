"""Module containing model definitions for server_monitoring application."""
from django.contrib.auth.models import User
from django.db import models


class Server(models.Model):
    """Model definition for Product.

        Fields:
            name (CharField): required;
            host (CharField): required;
            status (CharField): required;
            owner (ForeignKey): required;
            created_at (DateTimeField): auto created date;
            updated_at (DateTimeField): auto updated date."""
    STATUS_CHOICES = [
        ("online", "Online"),
        ("offline", "Offline"),
    ]
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="online")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="servers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Returns string representation of Server."""
        return self.name


class ServerMetric(models.Model):
    """Model definition for ServerMetric.

        Fields:
            server (ForeignKey): required;
            cpu_usage (DecimalField): required;
            memory_usage (DecimalField): required;
            load_average (DecimalField): required;
            recorded_at (DateTimeField): auto created date."""
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="metrics")
    cpu_usage = models.DecimalField(max_digits=5, decimal_places=2)
    memory_usage = models.DecimalField(max_digits=5, decimal_places=2)
    load_average = models.DecimalField(max_digits=5, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Returns string representation of ServerMetric."""
        return f"Metrics for {self.server.name}"

    @property
    def is_critical(self) -> bool:
        """Checks whether any metric is above critical threshold."""
        return any(
            value >= 90
            for value in (self.cpu_usage, self.memory_usage, self.load_average)
        )


class Alert(models.Model):
    """Model definition for Alert.

        Fields:
            server (ForeignKey): required;
            message (CharField): required;
            created_at (DateTimeField): auto created date."""
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="alerts")
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Returns string representation of Alert."""
        return f"Alert for {self.server.name}"
