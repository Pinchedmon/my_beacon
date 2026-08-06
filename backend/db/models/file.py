from typing import TYPE_CHECKING

from db.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.favourite import Favourite
    from db.models.note import Note

class File(Base):
    __tablename__ = "file"

    id: Mapped[int] = mapped_column(primary_key=True)
    minio_id: Mapped[str] = mapped_column(String(255), unique=True)
    note_id: Mapped[int | None] = mapped_column(
        ForeignKey("note.id", ondelete="CASCADE"), nullable=True, index=True
    )
    favourite_id: Mapped[int | None] = mapped_column(
        ForeignKey("favourite.id", ondelete="CASCADE"), nullable=True, index=True
    )

    note: Mapped[Note | None] = relationship(back_populates="files")
    favourite: Mapped[Favourite | None] = relationship(back_populates="files")

    def __repr__(self) -> str:
        return f"<File id={self.id}>"
