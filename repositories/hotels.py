from repositories.base import BaseRepository
from repositories.utils import rooms_ids_for_booking
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.schemas.hotels import Hotels
from datetime import date


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotels

    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset) -> list[Hotels]:

        query = select(HotelsOrm)
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(func.lower(title)))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(func.lower(location)))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            limit:int,
            offset:int):

        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        hotels_ids_to_get = (hotels_ids_to_get.limit(limit).offset(offset))
        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))
