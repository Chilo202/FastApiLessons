from datetime import date
from sqlalchemy import select
from src.exceptions import ObjectNotFoundException
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.models.booking import BookingsOrm

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingsAddRequest


class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_booking_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]

    async def add_booking(self, data: BookingsAddRequest, hotel_id: int):
        query = rooms_ids_for_booking(
            date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id
        )
        result = await self.session.execute(query)
        available_rooms_ids: list[int] = result.scalars().all()
        if data.room_id in available_rooms_ids:
            return await self.add(data)

        raise ObjectNotFoundException("Room is booked")
