from repositories.base import BaseRepository
from src.models.rooms import RoomsOrm


class RoomRepository(BaseRepository):
    model = RoomsOrm
