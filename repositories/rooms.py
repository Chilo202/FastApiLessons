from repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Rooms
from sqlalchemy import func, select


class RoomRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_all(self,
                      hotel_id,
                      title,
                      price,
                      quantity,
                      description,
                      limit,
                      offset) -> list[Rooms]:

        query = select(RoomsOrm)
        if title:
            query = query.filter(func.lower(RoomsOrm.title).contains(func.lower(title)))
        if description:
            query = query.filter(func.lower(RoomsOrm.description).contains(func.lower(description)))
        if price:
            query = query.filter(RoomsOrm.price == price)
        if quantity:
            query = query.filter(RoomsOrm.quantity == quantity)
        if hotel_id:
            query = query.filter(RoomsOrm.hotel_id == hotel_id)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]
