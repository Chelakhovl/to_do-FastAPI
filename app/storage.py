from threading import Lock
from typing import Dict, List, Optional
from .models import Task, TaskCreate, TaskUpdate


class InMemoryTaskStorage:
    """Thread-safe in-memory CRUD repository for tasks."""

    def __init__(self) -> None:
        """Initialize the in-memory storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = Lock()

    def list(self) -> List[Task]:
        """Return all tasks."""
        with self._lock:
            return list(self._tasks.values())

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        with self._lock:
            return self._tasks.get(task_id)

    def create(self, data: TaskCreate) -> Task:
        """Create a new task."""
        with self._lock:
            task = Task(id=self._next_id, **data.model_dump())
            self._tasks[self._next_id] = task
            self._next_id += 1
            return task

    def update(self, task_id: int, data: TaskUpdate) -> Optional[Task]:
        """Update an existing task."""
        with self._lock:
            existing = self._tasks.get(task_id)
            if not existing:
                return None
            updated_data = existing.model_dump()
            updated_data.update(data.model_dump(exclude_unset=True))
            updated = Task(**updated_data)
            self._tasks[task_id] = updated
            return updated

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID."""
        with self._lock:
            return self._tasks.pop(task_id, None) is not None


# Shared singleton instance
storage = InMemoryTaskStorage()
