from fastapi import FastAPI, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks(limit: int = 2, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM tasks"))
    tasks = result.mappings().all()
    return tasks[:limit]

@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM tasks WHERE id = :id"), {"id": task_id})
    task = result.mappings().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/tasks/status/{status}")
def get_task_by_status(status:str, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM tasks where status = :status"), {"status" : status})
    task = result.mappings().all()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", status_code=201)
def create_task(task: dict, db: Session = Depends(get_db)):
    db.execute(text("INSERT INTO tasks (tittle, status) VALUES (:tittle, :status)"), {"tittle": task["tittle"], "status": task["status"]})
    db.commit()
    return {"message": "Task created successfully"}



