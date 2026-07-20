from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
app = FastAPI(
    title="Task API",
    description="Simple CRUD API using FastAPI",
    version="1.0"
)
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Push to GitHub", "done": False}
]
class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
@app.get("/", summary="API Information")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }
@app.get("/health", summary="Health Check")
def health():
    return {"status": "ok"}
@app.get("/tasks", summary="Get All Tasks")
def get_tasks():
    return tasks
@app.get("/tasks/{task_id}", summary="Get Task By ID")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
@app.post("/tasks", status_code=201, summary="Create Task")
def create_task(task: TaskCreate):
    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
    new_task = {
        "id": max([t["id"] for t in tasks], default=0) + 1,
        "title": task.title,
        "done": False      
    }
    tasks.append(new_task)
    return new_task
@app.put("/tasks/{task_id}", summary="Update Task")
def update_task(task_id: int, updated: TaskUpdate):
    if updated.title is None and updated.done is None:
        raise HTTPException(
            status_code=400,
            detail="Request body cannot be empty"
        )           
    for task in tasks:
        if task["id"] == task_id:
            if updated.title is not None:
                if updated.title.strip() == "":
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )
                task["title"] = updated.title
            if updated.done is not None:
                task["done"] = updated.done
            return task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
@app.delete("/tasks/{task_id}", status_code=204, summary="Delete Task")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=204)
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
