import logging

from src.exceptions import ObjectNotFoundException, check_date_to_after_date_from, AllRoomsAreBookedException
from src.schemas.bookings import BookingsRequest
from src.services.base import BaseService


class BookingService(BaseService):

    async def book_room(self, booking_data, user_id):

        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise
        hotel = await self.db.hotels.get_one_or_none(id=room.hotel_id)
        check_date_to_after_date_from(booking_data.date_to, booking_data.date_from)
        _booking_data = BookingsRequest(
            user_id=user_id, price=room.price, **booking_data.model_dump()
        )
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
            await self.db.commit()
            return booking
        except AllRoomsAreBookedException:
            logging.error(f" All rooms are booked from {_booking_data.date_from} to {booking_data.date_to} room_id: {_booking_data.room_id}")
            raise


    async def get_my_books(self, user_id):
        return await self.db.bookings.get_filtered(user_id=user_id)


    async def get_all_books(self):
        return await self.db.bookings.get_all()

