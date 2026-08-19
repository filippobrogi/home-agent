import datetime

import pytest

from task_manager.task.models import TaskPriority
from task_manager.task.service import InMemoryTaskRepository


@pytest.mark.asyncio
async def test_create_task():
    repo = InMemoryTaskRepository()
    current_date = datetime.datetime.now() + datetime.timedelta(
        days=1
    )  # Ensure due_date is in the future
    task = await repo.create_task(
        "Test Task", "This is a test task.", current_date, TaskPriority.HIGH
    )
    assert task.title == "Test Task"
    assert task.description == "This is a test task."
    assert task.priority == TaskPriority.HIGH
    assert not task.completed


@pytest.mark.asyncio
async def test_get_task_by_id():
    repo = InMemoryTaskRepository()
    current_date = datetime.datetime.now() + datetime.timedelta(
        days=1
    )  # Ensure due_date is in the future
    created_task = await repo.create_task(
        "Test Task", "This is a test task.", current_date, TaskPriority.HIGH
    )
    retrieved_task = await repo.get_task_by_id(created_task.id)
    assert retrieved_task == created_task


@pytest.mark.asyncio
async def test_get_task_by_title():
    repo = InMemoryTaskRepository()
    current_date = datetime.datetime.now() + datetime.timedelta(
        days=1
    )  # Ensure due_date is in the future
    created_task = await repo.create_task(
        "Unique Task Title", "This is a test task.", current_date, TaskPriority.HIGH
    )
    retrieved_task = await repo.get_task_by_title("Unique Task Title")
    assert retrieved_task == created_task


@pytest.mark.asyncio
async def test_get_all_tasks():
    repo = InMemoryTaskRepository()
    current_date = datetime.datetime.now() + datetime.timedelta(
        days=1
    )  # Ensure due_date is in the future
    task1 = await repo.create_task("Task 1", "First task.", current_date, TaskPriority.LOW)
    task2 = await repo.create_task("Task 2", "Second task.", current_date, TaskPriority.MEDIUM)
    all_tasks = await repo.get_all_tasks()
    assert len(all_tasks) == 2
    assert task1 in all_tasks
    assert task2 in all_tasks


@pytest.mark.asyncio
async def test_update_task():
    repo = InMemoryTaskRepository()
    current_date = datetime.datetime.now() + datetime.timedelta(
        days=1
    )  # Ensure due_date is in the future
    task = await repo.create_task("Old Title", "Old description.", current_date, TaskPriority.LOW)
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
