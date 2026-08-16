import pytest

from task_manager.task.factory import get_task_repository
from task_manager.task.models import TaskPriority
from task_manager.task.service import InMemoryTaskRepository


def test_get_task_repository_singleton():
    repo1 = get_task_repository()
    repo2 = get_task_repository()
    assert repo1 is repo2
    assert isinstance(repo1, InMemoryTaskRepository)


@pytest.mark.asyncio
async def test_create_task():
    repo = InMemoryTaskRepository()
    task = await repo.create_task("Test Task", "This is a test task.", TaskPriority.HIGH)
    assert task.title == "Test Task"
    assert task.description == "This is a test task."
    assert task.priority == TaskPriority.HIGH
    assert not task.completed


@pytest.mark.asyncio
async def test_get_task():
    repo = InMemoryTaskRepository()
    created_task = await repo.create_task("Test Task", "This is a test task.", TaskPriority.HIGH)
    retrieved_task = await repo.get_task(created_task.id)
    assert retrieved_task == created_task


@pytest.mark.asyncio
async def test_get_all_tasks():
    repo = InMemoryTaskRepository()
    task1 = await repo.create_task("Task 1", "First task.", TaskPriority.LOW)
    task2 = await repo.create_task("Task 2", "Second task.", TaskPriority.MEDIUM)
    all_tasks = await repo.get_all_tasks()
    assert len(all_tasks) == 2
    assert task1 in all_tasks
    assert task2 in all_tasks


@pytest.mark.asyncio
async def test_update_task():
    repo = InMemoryTaskRepository()
    task = await repo.create_task("Old Title", "Old description.", TaskPriority.LOW)
    updated_task = await repo.update_task(
        task.id,
        title="New Title",
        description="New description.",
        priority=TaskPriority.HIGH,
        completed=True,
    )
    assert updated_task.title == "New Title"
    assert updated_task.description == "New description."
    assert updated_task.priority == TaskPriority.HIGH
    assert updated_task.completed
