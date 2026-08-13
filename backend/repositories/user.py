from logging import getLogger

from db.models.user import User
from repositories.base import BaseRepository

logger = getLogger(__name__)


class UserRepository(BaseRepository[User]):
    model = User
