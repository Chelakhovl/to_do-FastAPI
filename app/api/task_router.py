from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Task, TaskCreate, TaskUpdate
from ..services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[Task])
def list_tasks():
    """Return all tasks."""
    return TaskService.list_tasks()


@router.post("/", response_model=Task, status_code=201)
def create_task(data: TaskCreate):
    """Create a new task."""
    return TaskService.create_task(data)


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate):
    """Update a task by ID."""
    task = TaskService.update_task(task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task by ID."""
    success = TaskService.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
