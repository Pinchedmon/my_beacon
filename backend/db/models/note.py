from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from db.models.file import File
    from db.models.tag import Tag
    from db.models.team import Team


class Note(Base):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    content: Mapped[dict] = mapped_column(JSONB, default=dict)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id", ondelete="CASCADE"), index=True)

    team: Mapped[Team] = relationship(back_populates="notes")
    files: Mapped[list[File]] = relationship(
        back_populates="note", cascade="all, delete-orphan", passive_deletes=True
    )
    tags: Mapped[list[Tag]] = relationship(back_populates="notes", secondary="tag_note")

    def __repr__(self) -> str:
        return f"<Note id={self.id} name={self.name} created_at={self.created_at}>"
