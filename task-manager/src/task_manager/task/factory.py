from task_manager.task.repository import TaskRepository
from task_manager.task.service import InMemoryTaskRepository


def get_task_repository() -> TaskRepository:
    """Instantiates and returns a TaskRepository instance. If volatile is True, an in-memory repository is returned; otherwise, a persistent repository can be implemented in the future.

    Args:
        volatile (bool, optional): the flag to use. Defaults to True.

    Returns:
        TaskRepository: the repository instance
    """
    global _task_repository
    if _task_repository is None:
        _task_repository = InMemoryTaskRepository()

    return _task_repository


_task_repository: TaskRepository = None
