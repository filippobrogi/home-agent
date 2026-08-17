import logging
from datetime import datetime

from task_manager.models import PrimaryKey
from task_manager.task.models import Task, TaskPriority
from task_manager.task.repository import TaskRepository

logger = logging.getLogger(__name__)


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self._tasks: dict[PrimaryKey, Task] = {}
        self._next_id: PrimaryKey = 1

    async def create_task(
        self,
        title: str,
        description: str,
        due_date: datetime,
        priority: TaskPriority = TaskPriority.MEDIUM,
    ) -> Task:
        """Create a new task with the given title, description, and priority.

        Args:
            title (str): the title of the task
            description (str): the detailed description of the task
            due_date (datetime): the due date of the task
            priority (TaskPriority, optional): the priority of the task. Defaults to TaskPriority.MEDIUM.

        Returns:
            Task: the created task
        """
        task = {
            "id": self._next_id,
            "title": title,
            "description": description,
            "priority": priority,
            "completed": False,
            "due_date": due_date,
        }
        new_task = Task(**task)
        self._tasks[self._next_id] = new_task
        self._next_id += 1
        return new_task

    async def get_task(self, task_id: PrimaryKey) -> Task | None:
        """Retrieve a task by its ID."""
        return self._tasks.get(task_id)

    async def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks."""
        return list(self._tasks.values())

    async def update_task(
        self,
        task_id: PrimaryKey,
        title: str | None = None,
        description: str | None = None,
        priority: TaskPriority | None = None,
        completed: bool | None = None,
    ) -> Task | None:
        """Update a task with the given ID.

        Args:
            task_id (PrimaryKey): The ID of the task to update
            title (str | None, optional): The new title for the task. Defaults to None.
            description (str | None, optional): The new description for the task. Defaults to None.
            priority (str | None, optional): The new priority for the task. Defaults to None.
            completed (bool | None, optional): The new completion status for the task. Defaults to None.

        Returns:
            Task | None: The updated task, or None if the task was not found.
        """
        task: Task | None = self._tasks.get(task_id)
        if task is None:
            logger.warning(f"Task with ID {task_id} not found for update.")
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if completed is not None:
            task.completed = completed

        self._tasks[task_id] = task
        return task

    async def delete_task(self, task_id: PrimaryKey) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
