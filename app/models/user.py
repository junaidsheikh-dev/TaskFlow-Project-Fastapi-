from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models import Task
    from app.models.team import Team


class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column(unique=True, nullable=False)
    full_name : Mapped[str] = mapped_column(nullable=False)

    # Define relationships
    teams : Mapped[list["Team"]] = relationship(secondary="team_members", back_populates="members")
    assigned_tasks : Mapped[list["Task"]] = relationship(back_populates="assignee")