from sqlalchemy import func, select
from repositories.base import BaseRepository
from repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_filtered_by_time(self, date_from, date_to, hotel_id):

        rooms_ids_to_get = rooms_ids_for_booking(hotel_id, date_from, date_to)

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))


