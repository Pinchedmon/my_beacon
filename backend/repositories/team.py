from logging import getLogger

from db.models.team import Team
from repositories.base import BaseRepository

logger = getLogger(__name__)


class TeamRepository(BaseRepository[Team]):
    model = Team
