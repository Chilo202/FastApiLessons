from fastapi import APIRouter, HTTPException

from src.Exceptions import RoomNotAvailable
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAddRequest, BookingsRequest

router = APIRouter(prefix="/bookings", tags=['Book room'])


@router.get('')
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get('/me')
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post('')
async def book_room(db: DBDep,
                    user_id: UserIdDep,
                    booking_data: BookingsAddRequest
                    ):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    if not room:
        raise HTTPException(status_code=404, detail=f'Room with id: {booking_data.room_id} not found')
    if booking_data.date_from > booking_data.date_to:
        raise HTTPException(status_code=404, detail='date_from cannot be later than date_to')
    _booking_data = BookingsRequest(user_id=user_id, price=room.price, **booking_data.model_dump())
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await db.commit()
        return {"status": "OK", "data": booking}
    except RoomNotAvailable:
        raise HTTPException(status_code=500, detail="Room not available for that period")
