from task_manager.task.factory import get_task_repository
from task_manager.task.service import InMemoryTaskRepository


def test_get_task_repository_singleton():
    repo1 = get_task_repository()
    repo2 = get_task_repository()
    assert repo1 is repo2
    assert isinstance(repo1, InMemoryTaskRepository)
