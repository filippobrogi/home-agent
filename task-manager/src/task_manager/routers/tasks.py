from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import ValidationError
from typing_extensions import Annotated

from task_manager.task.factory import get_task_repository
from task_manager.task.models import Task
from task_manager.task.repository import TaskRepository

router = APIRouter()


@router.get("/tasks")
async def get_tasks(repository: Annotated[TaskRepository, Depends(get_task_repository)]):
    tasks = await repository.get_all_tasks()
    return {"tasks": tasks}


@router.post("/tasks", responses={400: {"description": "Invalid data"}})
async def create_task(
    repository: Annotated[TaskRepository, Depends(get_task_repository)],
    title: str,
    description: str,
    due_date: datetime,
):
    # Implementation for creating a task
    try:
        task = await repository.create_task(title=title, description=description, due_date=due_date)
        return {"task": task}
    except ValidationError as ex:
        raise HTTPException(status_code=400, detail=f"{ex}")


@router.patch(
    "/tasks/{task_id}", response_model=Task, responses={404: {"description": "Task not found"}}
)
async def update_task(
    task_id: int, repository: Annotated[TaskRepository, Depends(get_task_repository)]
):
    # Implementation for updating a task
    if task_id is None:
        raise HTTPException(status_code=400, detail="Task ID is required")

    task = await repository.get_task(task_id)
    return {"task": task}
