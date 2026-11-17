from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime



class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in progress"
    completed = "completed"
    todo = "todo"


class TaskCreate(BaseModel):
    title: str = Field(min_length = 3, max_length = 50)
    status: TaskStatus = TaskStatus.pending
    description: str | None = Field(default = None, min_length = 3, max_length = 200)
    priority: int = Field(default=3, ge=1, le=5)
    project_id: int | None = None
    assignee_id: int | None = None



class TaskResponse(TaskCreate):
    id: int
    title: str
    status: TaskStatus
    priority: int
    description: str | None = None
    project_id: int | None = None
    assignee_id: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskUpdate(BaseModel):
    title: str | None = Field(default = None, min_length = 3, max_length = 50)
    status: TaskStatus | None = None
    description: str | None = Field(default = None, min_length = 3, max_length = 200)
    priority: int | None = Field(default=None, ge=1, le=5)
    project_id: int | None = None
    assignee_id: int | None = None

class TaskPage(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int