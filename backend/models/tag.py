from db.db import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    notes: Mapped[list["Note"]] = relationship(back_populates="tags", secondary="tag_note")
    favourites: Mapped[list["Favourite"]] = relationship(
        back_populates="tags", secondary="tag_favourite"
    )
    routes: Mapped[list["Route"]] = relationship(back_populates="tags", secondary="tag_route")

    def __repr__(self) -> str:
        return f"<Tag id={self.id} name={self.name}>"
