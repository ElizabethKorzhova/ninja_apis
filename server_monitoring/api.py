"""This module contains API routes for server_monitoring application."""
from typing import List, Optional, Tuple

from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Alert, Server, ServerMetric
from .schemas import (
    AlertOut,
    ServerDetailsOut,
    ServerIn,
    ServerMetricIn,
    ServerMetricOut,
    ServerOut,
    ServerUpdate,
)

router = Router(tags=["Server Monitoring"])


@router.get("/servers/", response=List[ServerOut])
def get_servers(request: HttpRequest, status: Optional[str] = None) -> QuerySet[Server]:
    """Gets authenticated user's servers."""
    servers = Server.objects.filter(owner=request.user)
    if status:
        servers = servers.filter(status=status)
    return servers.order_by("-created_at")


@router.get("/servers/{server_id}", response={200: ServerDetailsOut})
def get_server(request: HttpRequest, server_id: int) -> Server:
    """Gets one server by id."""
    return get_object_or_404(
        Server.objects.prefetch_related("metrics", "alerts"),
        id=server_id,
        owner=request.user,
    )


@router.post("/servers/", response={201: ServerOut})
def create_server(request: HttpRequest, payload: ServerIn) -> Tuple[int, Server]:
    """Creates a new server."""
    server = Server.objects.create(owner=request.user, **payload.dict())
    return 201, server


@router.patch("/servers/{server_id}", response={200: ServerOut})
def update_server(
    request: HttpRequest,
    server_id: int,
    payload: ServerUpdate,
) -> Server:
    """Partially updates server by id."""
    server = get_object_or_404(Server, id=server_id, owner=request.user)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(server, field, value)

    server.save()
    return server


@router.delete("/servers/{server_id}", response={204: None})
def delete_server(request: HttpRequest, server_id: int) -> Tuple[int, None]:
    """Deletes server by id."""
    server = get_object_or_404(Server, id=server_id, owner=request.user)
    server.delete()
    return 204, None


@router.get("/servers/{server_id}/metrics/", response=List[ServerMetricOut])
def get_server_metrics(
    request: HttpRequest,
    server_id: int,
    critical_only: bool = False,
) -> list[ServerMetric]:
    """Gets server metrics."""
    server = get_object_or_404(Server, id=server_id, owner=request.user)
    metrics = list(server.metrics.order_by("-recorded_at"))
    if critical_only:
        metrics = [metric for metric in metrics if metric.is_critical]
    return metrics


@router.post("/servers/{server_id}/metrics/", response={201: ServerMetricOut})
def create_server_metric(
    request: HttpRequest,
    server_id: int,
    payload: ServerMetricIn,
) -> Tuple[int, ServerMetric]:
    """Creates a new metric for server and generates alert if needed."""
    server = get_object_or_404(Server, id=server_id, owner=request.user)
    metric = ServerMetric.objects.create(server=server, **payload.dict())

    if metric.is_critical:
        Alert.objects.create(
            server=server,
            message="Critical metric threshold reached.",
        )

    return 201, metric


@router.get("/servers/{server_id}/alerts/", response=List[AlertOut])
def get_server_alerts(
    request: HttpRequest,
    server_id: int,
) -> QuerySet[Alert]:
    """Gets alerts for server."""
    server = get_object_or_404(Server, id=server_id, owner=request.user)
    return server.alerts.order_by("-created_at")
