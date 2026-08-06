from typing import TYPE_CHECKING

from db.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.favourite import Favourite
    from db.models.note import Note
    from db.models.route import Route
    from db.models.user import User

class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    users: Mapped[list[User]] = relationship(secondary="user_team", back_populates="teams")
    notes: Mapped[list[Note]] = relationship(back_populates="team", cascade="all, delete-orphan", passive_deletes=True)
    routes: Mapped[list[Route]] = relationship(
        back_populates="team", cascade="all, delete-orphan", passive_deletes=True
    )
    favourites: Mapped[list[Favourite]] = relationship(
        back_populates="team", cascade="all, delete-orphan", passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"<Team id={self.id} name={self.name}>"
