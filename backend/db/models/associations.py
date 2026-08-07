from sqlalchemy import Column, ForeignKey, Index, Table

from db.base import Base

user_team_association = Table(
    "user_team",
    Base.metadata,
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    Column("team_id", ForeignKey("team.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_user_team_team_id", "team_id"),
)

tag_note_association = Table(
    "tag_note",
    Base.metadata,
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
    Column("note_id", ForeignKey("note.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_tag_note_note_id", "note_id"),
)

tag_route_association = Table(
    "tag_route",
    Base.metadata,
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
    Column("route_id", ForeignKey("route.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_tag_route_route_id", "route_id"),
)

tag_favourite_association = Table(
    "tag_favourite",
    Base.metadata,
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
    Column("favourite_id", ForeignKey("favourite.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_tag_favourite_favourite_id", "favourite_id"),
)

like_user_association = Table(
    "like_user",
    Base.metadata,
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    Column("favourite_id", ForeignKey("favourite.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_like_user_favourite_id", "favourite_id"),
)
