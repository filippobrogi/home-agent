from abc import ABC, abstractmethod
from datetime import datetime

from task_manager.models import PrimaryKey
from task_manager.task.models import Task, TaskPriority


class TaskRepository(ABC):
    """Interface for task repository."""

    @abstractmethod
    async def create_task(
        self,
        title: str,
        description: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        due_date: datetime | None = None,
    ) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def get_task(self, task_id: PrimaryKey) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_tasks(self) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    async def update_task(
        self,
        task_id: PrimaryKey,
        title: str | None = None,
        description: str | None = None,
        priority: TaskPriority | None = None,
        completed: bool | None = None,
        due_date: datetime | None = None,
    ) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, task_id: PrimaryKey) -> bool:
        raise NotImplementedError
