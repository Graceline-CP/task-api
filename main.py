from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build Task API", "done": False},
    {"id": 3, "title": "Test the API", "done": True}
]

class TaskCreate(BaseModel):
    title: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

@app.get("/", summary="API information")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", summary="Get a task by ID")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required and cannot be empty"
        )

    new_id = max(t["id"] for t in tasks) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:

            if task_update.title is None and task_update.done is None:
                raise HTTPException(
                    status_code=400,
                    detail="At least one field is required"
                )

            if task_update.title is not None:
                if not task_update.title.strip():
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )
                task["title"] = task_update.title

            if task_update.done is not None:
                task["done"] = task_update.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )