from repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Rooms


class RoomRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms



