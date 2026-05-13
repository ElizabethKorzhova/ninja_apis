"""This module contains API routes for task_manager application."""
from typing import Literal, Optional, List, Tuple

from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Task
from .schemas import TaskIn, TaskOut, TaskUpdate

router = Router(tags=["Task Manager"])


@router.get("/", response=List[TaskOut])
def get_tasks(
    request: HttpRequest,
    status: Optional[str] = None,
    ordering: Optional[
        Literal[
            "created_at",
            "-created_at",
            "due_date",
            "-due_date",
        ]
    ] = "-created_at",
) -> QuerySet[Task]:
    """Gets authenticated user's tasks."""
    tasks = Task.objects.filter(owner=request.user)
    if status:
        tasks = tasks.filter(status=status)
    return tasks.order_by(ordering)


@router.get("/{task_id}", response={200: TaskOut})
def get_task(request: HttpRequest, task_id: int) -> Task:
    """Gets one task by id."""
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    return task


@router.post("/", response={201: TaskOut})
def create_task(request: HttpRequest, payload: TaskIn) -> Tuple[int, Task]:
    """Creates a new task."""
    task = Task.objects.create(owner=request.user, **payload.dict())
    return 201, task


@router.patch("/{task_id}", response={200: TaskOut})
def update_task(request: HttpRequest, task_id: int, payload: TaskUpdate) -> Task:
    """Partially updates task by id."""
    task = get_object_or_404(Task, id=task_id, owner=request.user)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(task, field, value)

    task.save()
    return task


@router.delete("/{task_id}", response={204: None})
def delete_task(request: HttpRequest, task_id: int) -> Tuple[int, None]:
    """Deletes task by id."""
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.delete()
    return 204, None
