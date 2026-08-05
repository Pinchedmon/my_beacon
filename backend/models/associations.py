from db.db import Base
from sqlalchemy import Column, ForeignKey, Table

user_team_association = Table(
    "user_team",
    Base.metadata,
    Column("users_id", ForeignKey("user.id"), primary_key=True),
    Column("teams_id", ForeignKey("team.id"), primary_key=True),
)

tag_note_association = Table(
    "tag_note",
    Base.metadata,
    Column("tags_id", ForeignKey("tag.id"), primary_key=True),
    Column("notes_id", ForeignKey("note.id"), primary_key=True),
)

tag_route_association = Table(
    "tag_route",
    Base.metadata,
    Column("tags_id", ForeignKey("tag.id"), primary_key=True),
    Column("routes_id", ForeignKey("route.id"), primary_key=True),
)

tag_favourite_association = Table(
    "tag_favourite",
    Base.metadata,
    Column("tags_id", ForeignKey("tag.id"), primary_key=True),
    Column("favourites_id", ForeignKey("favourite.id"), primary_key=True),
)

like_user_association = Table(
    "like_user",
    Base.metadata,
    Column("users_id", ForeignKey("user.id"), primary_key=True),
    Column("favourites_id", ForeignKey("favourite.id"), primary_key=True),
)
