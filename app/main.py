from fastapi import FastAPI
from app.routers import tasks
from app.database import engine, Base



app = FastAPI()

app.include_router(tasks.router)