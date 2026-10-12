from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import Project


class Team(Base):
    __tablename__ = "teams"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(unique=True, nullable=False)


    # Define relationships
    members : Mapped[list["User"]] = relationship(secondary="team_members", back_populates="teams")
    projects : Mapped[list["Project"]] = relationship(back_populates="team", cascade="all, delete-orphan")