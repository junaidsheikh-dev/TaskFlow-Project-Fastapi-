from pydantic import BaseModel, Field
from enum import Enum



class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in progress"
    completed = "completed"


class CreateTask(BaseModel):
    title: str = Field(min_length = 3, max_length = 50)
    status: StatusEnum = StatusEnum.pending


class ResponseTask(CreateTask):
    id: int


class UpdateTask(BaseModel):
    title: str | None = Field(default = None, min_length = 3, max_length = 50)
    status: StatusEnum | None = None