from datetime import date

from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.models.booking import BookingsOrm


class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper


    async def get_booking_with_today_checkin(self):
        query = (select(BookingsOrm)
                 .filter(BookingsOrm.date_from == date.today()))
        res = await self.session.execute(query)
        print(query.compile(compile_kwargs={"literal_binds": True} ))
        return  [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]