from fastapi import FastAPI, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
import schemas
from routers import tasks

app = FastAPI()


app.include_router(tasks.router)