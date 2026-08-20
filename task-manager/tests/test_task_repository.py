from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from task_manager.task.models import TaskPriority
from task_manager.task.service import InMemoryTaskRepository


@pytest.mark.asyncio
async def test_create_task():
    repo = InMemoryTaskRepository()
    current_date = datetime.now() + timedelta(days=1)  # Ensure due_date is in the future
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
    current_date = datetime.now() + timedelta(days=1)  # Ensure due_date is in the future
    created_task = await repo.create_task(
        "Test Task", "This is a test task.", current_date, TaskPriority.HIGH
    )
    retrieved_task = await repo.get_task_by_id(created_task.id)
    assert retrieved_task == created_task


@pytest.mark.asyncio
async def test_get_task_by_title():
    repo = InMemoryTaskRepository()
    current_date = datetime.now() + timedelta(days=1)  # Ensure due_date is in the future
    created_task = await repo.create_task(
        "Unique Task Title", "This is a test task.", current_date, TaskPriority.HIGH
    )
    retrieved_task = await repo.get_task_by_title("Unique Task Title")
    assert retrieved_task == created_task


@pytest.mark.asyncio
async def test_get_all_tasks():
    repo = InMemoryTaskRepository()
    current_date = datetime.now() + timedelta(days=1)  # Ensure due_date is in the future
    task1 = await repo.create_task("Task 1", "First task.", current_date, TaskPriority.LOW)
    task2 = await repo.create_task("Task 2", "Second task.", current_date, TaskPriority.MEDIUM)
    all_tasks = await repo.get_all_tasks()
    assert len(all_tasks) == 2
    assert task1 in all_tasks
    assert task2 in all_tasks


@pytest.mark.asyncio
async def test_update_task():
    repo = InMemoryTaskRepository()
    current_date = datetime.now() + timedelta(days=1)  # Ensure due_date is in the future
    task = await repo.create_task("Old Title", "Old description.", current_date, TaskPriority.LOW)
    updated_task = await repo.update_task(
        task.id,
        title="New Title",
        description="New description.",
        priority=TaskPriority.HIGH,
        due_date=current_date + timedelta(days=1),
    )
    assert updated_task.title == "New Title"
    assert updated_task.description == "New description."
    assert updated_task.priority == TaskPriority.HIGH
    assert updated_task.due_date == current_date + timedelta(days=1)
    assert not updated_task.completed


@pytest.mark.asyncio
async def test_complete_task():
    repo = InMemoryTaskRepository()
    current_date = datetime.now() + timedelta(days=1)  # Ensure due_date is in the future
    task = await repo.create_task(
        "Incomplete Task", "This task is not completed.", current_date, TaskPriority.MEDIUM
    )
    result = await repo.complete_task(task.id)
    assert result is True
    completed_task = await repo.get_task_by_id(task.id)
    assert completed_task.completed is True


@pytest.mark.asyncio
async def test_delete_task():
    repo = InMemoryTaskRepository()
    current_date = datetime.now() + timedelta(days=1)  # Ensure due_date is in the future
    task = await repo.create_task(
        "Task to Delete", "This task will be deleted.", current_date, TaskPriority.LOW
    )
    result = await repo.delete_task(task.id)
    assert result is True
    deleted_task = await repo.get_task_by_id(task.id)
    assert deleted_task is None


@pytest.mark.asyncio
@patch.object(InMemoryTaskRepository, "_current_datetime")
async def test_get_overdue_tasks(mocked_datetime_now):
    mocked_datetime_now.return_value = datetime.now() + timedelta(days=1, hours=12)
    # to test this one we need to mock the datetime now() function to return a fixed date in the future, so we can create tasks with due dates in the past and future. However, for simplicity, we will create tasks with due dates in the past and future relative to the current time.
    repo = InMemoryTaskRepository()
    past_date = datetime.now() + timedelta(days=1)  # Ensure due_date is in the past
    future_date = datetime.now() + timedelta(days=2)  # Ensure due_date is in the future

    overdue_task = await repo.create_task(
        "Overdue Task", "This task is overdue.", past_date, TaskPriority.HIGH
    )
    not_overdue_task = await repo.create_task(
        "Not Overdue Task", "This task is not overdue.", future_date, TaskPriority.LOW
    )

    overdue_tasks = await repo.get_overdue_tasks()
    assert len(overdue_tasks) == 1
    assert overdue_task in overdue_tasks
    assert not_overdue_task not in overdue_tasks
