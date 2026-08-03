from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.db import Base


class Favourite(Base):
    __tablename__ = "favourite"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    content: Mapped[dict] = mapped_column(JSONB, default=dict)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    done: Mapped[bool] = mapped_column(Boolean, default=False)

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

    team: Mapped["Team"] = relationship(back_populates="favourites")
    files: Mapped[list["File"]] = relationship(
        back_populates="favourite", cascade="all, delete-orphan"
    )
    tags: Mapped[list["Tag"]] = relationship(back_populates="favourites", secondary="tag_favourite")
    user_likes: Mapped[list["User"]] = relationship(
        back_populates="favourites", secondary="like_user"
    )

    def __repr__(self) -> str:
        return f"<Favourite id={self.id} name={self.name} created_at={self.created_at}>"
