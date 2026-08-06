from typing import TYPE_CHECKING

from db.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.favourite import Favourite
    from db.models.team import Team

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(255))

    teams: Mapped[list[Team]] = relationship(secondary="user_team", back_populates="users")
    favourites: Mapped[list[Favourite]] = relationship(
        back_populates="user_likes", secondary="like_user"
    )
