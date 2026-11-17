from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import EmailAlreadyRegisteredError
from app.models.user import User
from app.schemas import UserCreate, UserResponse
from app.security import hash_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Register a new user",
)
async def register(data: UserCreate, db: Session = Depends(get_db)):
    """Creates a user account. The password is hashed and never stored or returned."""
    user = User(
        email=data.email.lower(),
        full_name=data.full_name,
        hashed_password=await run_in_threadpool(hash_password, data.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise EmailAlreadyRegisteredError(data.email)
    finally:
        db.refresh(user)
    return user