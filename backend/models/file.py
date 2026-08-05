from db.db import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class File(Base):
    __tablename__ = "file"

    id: Mapped[int] = mapped_column(primary_key=True)
    minio_id: Mapped[str] = mapped_column(String(255), unique=True)
    note_id: Mapped[int | None] = mapped_column(ForeignKey("note.id"), nullable=True)
    favourite_id: Mapped[int | None] = mapped_column(ForeignKey("favourite.id"), nullable=True)

    note: Mapped["Note"] = relationship(back_populates="files")
    favourite: Mapped["Favourite"] = relationship(back_populates="files")

    def __repr__(self) -> str:
        return f"<File id={self.id}>"
