from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

app = FastAPI(title="Task Manager API", version="1.0.0") 
class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
 
class Task(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1, max_length=120, description="Required text for the task name.")
    description: Optional[str] = Field(default=None, description="Optional extra information.")
    status: TaskStatus = Field(default=TaskStatus.todo, description="todo, in_progress or done.")
    priority: int = Field(default=3, ge=1, le=5, description="An integer from 1 to 5.")

# In-memory database
fake_tasks_db = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager REST API"}
 
@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return fake_tasks_db
 
@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    task_dict = task.model_dump()
    task_dict["id"] = len(fake_tasks_db) + 1
    fake_tasks_db.append(task_dict)
    return task_dict
 
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    for task in fake_tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found") 
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    for index, existing_task in enumerate(fake_tasks_db):
        if existing_task["id"] == task_id:
            updated_task = task.model_dump()
            updated_task["id"] = task_id
            fake_tasks_db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
 
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(fake_tasks_db):
        if task["id"] == task_id:
            fake_tasks_db.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")