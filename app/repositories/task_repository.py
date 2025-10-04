from typing import Protocol, List, Optional
from ..models import Task, TaskCreate, TaskUpdate


class ITaskRepository(Protocol):
    """Interface for any Task repository implementation (in-memory, Postgres, etc.)."""

    def list(self) -> List[Task]:
        """Return all tasks."""
        ...

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        ...

    def create(self, data: TaskCreate) -> Task:
        """Create a new task."""
        ...

    def update(self, task_id: int, data: TaskUpdate) -> Optional[Task]:
        """Update an existing task."""
        ...

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID."""
        ...
