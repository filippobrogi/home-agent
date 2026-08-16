from fastapi import FastAPI

from task_manager.logging import configure_logging
from task_manager.routers import tasks

__VERSION__ = "0.0.1"

app = FastAPI(title="Task Manager API", description="API for managing tasks", version=__VERSION__)


configure_logging()


@app.get("/")
async def read_root():
    return {"message": f"Welcome to the Task Manager API v{__VERSION__}!"}


# Adding the routers
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])
