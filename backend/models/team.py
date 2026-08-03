from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.db import Base


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    users: Mapped[list["User"]] = relationship(secondary="user_team", back_populates="teams")
    notes: Mapped[list["Note"]] = relationship(back_populates="team", cascade="all, delete-orphan")
    routes: Mapped[list["Route"]] = relationship(
        back_populates="team", cascade="all, delete-orphan"
    )
    favourites: Mapped[list["Favourite"]] = relationship(
        back_populates="team", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Team id={self.id} name={self.name}>"
