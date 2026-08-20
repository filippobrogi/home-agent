from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import ValidationError
from typing_extensions import Annotated

from task_manager.task.factory import get_task_repository
from task_manager.task.models import Task, UpdateTask
from task_manager.task.repository import TaskRepository

router = APIRouter()


@router.get("/tasks", description="Retrieve all tasks", response_model=dict)
async def get_tasks(
    repository: Annotated[TaskRepository, Depends(get_task_repository)], overdue: bool = False
):
    if overdue:
        tasks = await repository.get_overdue_tasks()
    else:
        tasks = await repository.get_all_tasks()
    return {"tasks": tasks}


@router.post(
    "/tasks",
    description="Create a new task",
    response_model=Task,
    responses={400: {"description": "Invalid data"}},
)
async def create_task(
    repository: Annotated[TaskRepository, Depends(get_task_repository)],
    title: str,
    description: str,
    due_date: datetime,
):
    try:
        task = await repository.create_task(title=title, description=description, due_date=due_date)
        return {"task": task}
    except ValidationError as ex:
        raise HTTPException(status_code=400, detail=f"{ex}")


@router.patch(
    "/tasks/{task_id}",
    description="Update an existing task",
    response_model=Task,
    responses={404: {"description": "Task not found"}},
)
async def update_task(
    task_id: int,
    update_data: UpdateTask,
    repository: Annotated[TaskRepository, Depends(get_task_repository)],
):
    # Implementation for updating a task
    task = await repository.update_task(task_id, **update_data.dict(exclude_unset=True))
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@router.post(
    "/tasks/{task_id}/complete",
    description="Mark a task as completed",
    response_model=dict,
    responses={404: {"description": "Task not found"}},
)
async def complete_task(
    task_id: int, repository: Annotated[TaskRepository, Depends(get_task_repository)]
):
    # Implementation for completing a task
    if not await repository.complete_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return {"message": f"Task {task_id} marked as completed"}


@router.get(
    "/tasks/{task_title}",
    description="Retrieve a task by title",
    response_model=Task,
    responses={404: {"description": "Task not found"}},
)
async def get_task(
    task_title: str, repository: Annotated[TaskRepository, Depends(get_task_repository)]
):
    # Implementation for retrieving a task
    if task_title is None:
        raise HTTPException(status_code=400, detail="Task title is required")

    task = await repository.get_task_by_title(task_title)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": task}


@router.delete(
    "/tasks/{task_id}",
    description="Delete a task",
    response_model=dict,
    responses={404: {"description": "Task not found"}},
)
async def delete_task(
    task_id: int, repository: Annotated[TaskRepository, Depends(get_task_repository)]
):
    # Implementation for deleting a task
    if not await repository.delete_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return {"message": f"Task {task_id} deleted successfully"}
