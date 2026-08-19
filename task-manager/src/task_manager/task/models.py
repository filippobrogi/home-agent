from enum import StrEnum

from pydantic import BaseModel, FutureDatetime, PositiveInt, field_validator

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
    duration: PositiveInt = 60
    priority: TaskPriority = TaskPriority.MEDIUM
    completed: bool = False

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v


class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: FutureDatetime | None = None
    duration: PositiveInt | None = None
    priority: TaskPriority | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v
