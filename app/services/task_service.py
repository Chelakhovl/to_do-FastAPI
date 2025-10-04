from typing import List, Optional
from ..models import Task, TaskCreate, TaskUpdate
from ..storage import storage
from ..repositories.task_repository import ITaskRepository


class TaskService:
    """Business logic for task management, independent of the storage implementation."""

    def __init__(self, repository: ITaskRepository = storage):
        """Initialize the service with a repository (in-memory or database)."""
        self.repository = repository

    def list_tasks(self) -> List[Task]:
        """Return all tasks."""
        return self.repository.list()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID."""
        return self.repository.get(task_id)

    def create_task(self, data: TaskCreate) -> Task:
        """Create a new task."""
        return self.repository.create(data)

    def update_task(self, task_id: int, data: TaskUpdate) -> Optional[Task]:
        """Update an existing task."""
        return self.repository.update(task_id, data)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        return self.repository.delete(task_id)
