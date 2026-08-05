from datetime import datetime

from db.db import Base
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Note(Base):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    content: Mapped[dict] = mapped_column(JSONB, default=dict)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

    team: Mapped["Team"] = relationship(back_populates="notes")
    files: Mapped[list["File"]] = relationship(back_populates="note", cascade="all, delete-orphan")
    tags: Mapped[list["Tag"]] = relationship(back_populates="notes", secondary="tag_note")

    def __repr__(self) -> str:
        return f"<Note id={self.id} name={self.name} created_at={self.created_at}>"
