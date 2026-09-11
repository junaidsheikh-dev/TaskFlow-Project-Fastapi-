from fastapi import FastAPI, HTTPException, Depends, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
import schemas


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/", response_model=list[schemas.ResponseTask])
def get_tasks(limit: int = 2, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM tasks"))
    tasks = result.mappings().all()
    return tasks[:limit]

@router.get("/{task_id}", response_model=schemas.ResponseTask)
def get_task(task_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM tasks WHERE id = :id"), {"id": task_id})
    task = result.mappings().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/status/{status}", response_model=list[schemas.ResponseTask])
def get_task_by_status(status:str, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM tasks where status = :status"), {"status" : status})
    task = result.mappings().all()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task



@router.post("/", status_code=201)
def create_task(task: schemas.CreateTask, db: Session = Depends(get_db)):
    db.execute(text("INSERT INTO tasks (title, status) VALUES (:title, :status)"), {"title": task.title, "status": task.status})
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
def update_task(task_id : int, task: schemas.UpdateTask, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM tasks WHERE id = :id"), {"id": task_id}).mappings().first()
    print(result)
    if not result:
            raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task.model_dump(exclude_unset=True)

    if "title" in update_data:
        db.execute(text("UPDATE tasks SET title = :title WHERE id = :id"), {"title": task.title, "id": task_id})

    if "status" in update_data:
        db.execute(text("UPDATE tasks SET status = :status WHERE id = :id"), {"status": task.status, "id": task_id})
    # db.execute(text("UPDATE tasks SET title = :title, status = :status WHERE id = :id"), {"title": task.title, "status": task.status, "id": task_id})
    
    db.commit()
    return {"message": "Task updated successfully"}