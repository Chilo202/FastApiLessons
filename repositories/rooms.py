from sqlalchemy import select
from repositories.base import BaseRepository
from repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Rooms, RoomsWithRels
from sqlalchemy.orm import selectinload
from datetime import date


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_filtered_by_time(self,
                                   date_from: date,
                                   date_to: date,
                                   hotel_id: int
                                   ):
        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

        query = (select(self.model)
                 .options(selectinload(self.model.facilities))
                 .filter(RoomsOrm.id.in_(rooms_ids_to_get)))

        result = await self.session.execute(query)

        return [RoomsWithRels.model_validate(model) for model in result.scalars().all()]

    async def get_room_with_facilities(self, **kwargs):
        query = (select(self.model)
                 .options(selectinload(self.model.facilities))
                 .filter_by(**kwargs))
        res = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if model is None:
            return None
        return RoomsWithRels.model_validate(model)
