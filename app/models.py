from pydantic import BaseModel, Field
from typing import Optional


class TaskBase(BaseModel):
    """Base fields shared by all Task models."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    done: bool = False


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    done: Optional[bool] = None


class Task(TaskBase):
    """Schema returned to the client."""

    id: int

    class Config:
        from_attributes = True  # enable ORM-style parsing
