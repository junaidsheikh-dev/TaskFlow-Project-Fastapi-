import math
from typing import Literal
from fastapi import FastAPI, HTTPException, Depends, APIRouter, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.models.task import Task          # adjust to your models layout
from app.schemas import (
    TaskCreate,
    TaskPage,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)



router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

TaskSort = Literal[
    "created_at", "-created_at",
    "priority", "-priority",
    "title", "-title",
]

SORT_COLUMNS = {
    "created_at": Task.created_at,
    "priority": Task.priority,
    "title": Task.title,
}


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/", response_model=TaskPage)
def get_tasks(
    status: TaskStatus | None = None,
    assignee_id: int | None = None,
    project_id: int | None = None,
    sort: TaskSort = "-created_at",
    page: int = Query(1, ge=1),
    page_size: int = 20,
    db: Session = Depends(get_db)):

    """Lists tasks with optional filters, sorting (prefix `-` for descending) and pagination."""
    filters = []
    if status is not None:
        filters.append(Task.status == status)
    if assignee_id is not None:
        filters.append(Task.assignee_id == assignee_id)
    if project_id is not None:
        filters.append(Task.project_id == project_id)

    total = db.scalar(select(func.count()).select_from(Task).where(*filters))

    column = SORT_COLUMNS[sort.lstrip("-")]
    order = column.desc() if sort.startswith("-") else column.asc()

    query = (
        select(Task)
        .where(*filters)
        .order_by(order, Task.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    tasks = (db.execute(query)).scalars().all()

    return TaskPage(
        items=[TaskResponse.model_validate(t) for t in tasks],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size),
    )

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM tasks WHERE id = :id"), {"id": task_id})
    task = result.mappings().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/status/{status}", response_model=list[TaskResponse])
def get_task_by_status(status:str, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM tasks where status = :status"), {"status" : status})
    task = result.mappings().all()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task



@router.post("/", status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db.execute(text("INSERT INTO tasks (title, status, description) VALUES (:title, :status, :description)"), {"title": task.title, "status": task.status, "description": task.description})
    db.commit()
    return {"message": "Task created successfully"}


@router.delete("/{task_id}", status_code=200)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    result =  db.execute(text("SELECT * FROM tasks WHERE id = :id"), {"id": task_id})
    if not result.mappings().first():
        raise HTTPException(status_code=404, detail="Task not found")
    db.execute(text("DELETE FROM tasks WHERE id = :id"), {"id": task_id})
    db.commit()

    return {"message": "Task deleted successfully"}



@router.delete("/delete/task", status_code=200)
def delete_task(status: str, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT* FROM tasks WHERE status = :status"), {"status" : status}) 
    if not result.mappings().first():
        raise HTTPException(status_code=404, detail="Task not found")
    db.execute(text("DELETE FROM tasks WHERE status = :status"), {"status" : status})
    db.commit()
    return {"message": "Task deleted successfully"}


@router.put("/{task_id}")
def update_task(task_id : int, task: TaskUpdate, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM tasks WHERE id = :id"), {"id": task_id}).mappings().first()
    print(result)
    if not result:
            raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task.model_dump(exclude_unset=True)

    if "title" in update_data:
        db.execute(text("UPDATE tasks SET title = :title WHERE id = :id"), {"title": task.title, "id": task_id})

    if "status" in update_data:
        db.execute(text("UPDATE tasks SET status = :status WHERE id = :id"), {"status": task.status, "id": task_id})

    if "description" in update_data:
        db.execute(text("UPDATE tasks SET description = :description WHERE id = :id"), {"description": task.description, "id": task_id})
    # db.execute(text("UPDATE tasks SET title = :title, status = :status WHERE id = :id"), {"title": task.title, "status": task.status, "id": task_id})
    
    db.commit()
    return {"message": "Task updated successfully"}