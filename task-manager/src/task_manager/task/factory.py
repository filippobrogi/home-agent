from task_manager.task.repository import TaskRepository
from task_manager.task.service import InMemoryTaskRepository


def get_task_repository(volatile: bool = True) -> TaskRepository:
    """Factory function to get the task repository."""
    global _task_repository
    if _task_repository is None:
        _task_repository = InMemoryTaskRepository()

    return _task_repository


_task_repository: TaskRepository = None
