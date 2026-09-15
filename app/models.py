from sqlalchemy import Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    status: Mapped[str] = mapped_column(default="todo")
    priority: Mapped[int] = mapped_column(default=3)
    description: Mapped[str | None] = mapped_column(default=None)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
