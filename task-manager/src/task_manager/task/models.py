from enum import StrEnum

from pydantic import BaseModel, FutureDatetime

from task_manager.models import PrimaryKey


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# I have to validate that the due_date is not in the past. Write a data validation method for the Task model that checks if the due_date is in the past and raises a ValueError if it is.
class Task(BaseModel):
    id: PrimaryKey
    title: str
    description: str
    due_date: FutureDatetime
    priority: TaskPriority = TaskPriority.MEDIUM
    completed: bool = False
