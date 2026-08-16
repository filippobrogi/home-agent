from enum import StrEnum

from pydantic import BaseModel

from task_manager.models import PrimaryKey


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(BaseModel):
    id: PrimaryKey
    title: str
    description: str
    priority: TaskPriority = TaskPriority.MEDIUM
    completed: bool = False
