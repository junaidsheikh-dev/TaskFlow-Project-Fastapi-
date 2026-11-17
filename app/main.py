from fastapi import FastAPI
from app.routers import tasks, auth
from app.exceptions import register_exception_handlers



app = FastAPI(title = "TaskFlow API", description = "A simple task management API built with FastAPI and SQLAlchemy", version = "1.0.0")

register_exception_handlers(app)

app.include_router(tasks.router)
app.include_router(auth.router)