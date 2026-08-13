from db.models.favourite import Favourite
from repositories.base import BaseRepository


class FavouriteRepository(BaseRepository[Favourite]):
    model = Favourite
