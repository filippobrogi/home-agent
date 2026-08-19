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
        duration: int = 60,
        due_date: datetime | None = None,
    ) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_id(self, task_id: PrimaryKey) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_title(self, title: str) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    async def get_overdue_tasks(self) -> list[Task]:
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
        duration: int = 60,
        due_date: datetime | None = None,
    ) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    async def complete_task(self, task_id: PrimaryKey) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, task_id: PrimaryKey) -> bool:
        raise NotImplementedError
