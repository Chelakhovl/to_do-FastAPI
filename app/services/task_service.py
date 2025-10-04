from typing import List, Optional
from ..models import Task, TaskCreate, TaskUpdate
from ..storage import storage
from ..repositories.task_repository import ITaskRepository


class TaskService:
    """Business logic layer for managing tasks."""

    def __init__(self, repository: ITaskRepository = storage):
        """Initialize the service with a repository (in-memory by default)."""
        self.repository = repository

    def list_tasks(self) -> List[Task]:
        """Return all tasks."""
        return self.repository.list()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Return a single task by ID or raise ValueError if not found."""
        task = self.repository.get(task_id)
        if not task:
            raise ValueError(f"Task with id={task_id} not found")
        return task

    def create_task(self, data: TaskCreate) -> Task:
        """Create a new task. Raise ValueError if title already exists."""
        existing_titles = [t.title.lower() for t in self.repository.list()]
        if data.title.lower() in existing_titles:
            raise ValueError("Task with this title already exists.")
        return self.repository.create(data)

    def update_task(self, task_id: int, data: TaskUpdate) -> Task:
        """Update a task by ID or raise ValueError if not found."""
        if not self.repository.get(task_id):
            raise ValueError(f"Task with id={task_id} not found")
        return self.repository.update(task_id, data)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID or raise ValueError if not found."""
        if not self.repository.get(task_id):
            raise ValueError(f"Task with id={task_id} not found")
        return self.repository.delete(task_id)
