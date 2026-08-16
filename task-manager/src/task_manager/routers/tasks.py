from fastapi import APIRouter

router = APIRouter()


@router.get("/tasks")
async def get_tasks():
    return {"message": "List of tasks"}


@router.post("/tasks")
async def create_task():
    return {"message": "Task created"}


@router.patch("/tasks/{task_id}")
async def update_task(task_id: int):
    return {"message": f"Task {task_id} updated"}
