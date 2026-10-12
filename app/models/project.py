from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.team import Team


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(default=None)
    team_id : Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)

    # Define relationships
    team: Mapped["Team"] = relationship(back_populates="projects")
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )