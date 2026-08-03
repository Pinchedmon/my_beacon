from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.db import Base


class Route(Base):
    __tablename__ = "route"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    points: Mapped[dict] = mapped_column(JSONB, default=dict)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    created_at : Mapped[datetime] = mapped_column(server_default=func.now())

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

    team:Mapped["Team"]= relationship(back_populates="routes")
    tags: Mapped[list["Tag"]] =relationship(back_populates="routes", secondary="tag_route")

    def __repr__(self) -> str:
        return f"<Route id={self.id} name={self.name} created_at={self.created_at}>"
