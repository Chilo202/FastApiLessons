from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAddRequest, BookingsRequest

router = APIRouter(prefix="/bookings", tags=['Book room'])


@router.post('')
async def book_room(db: DBDep, user_id: UserIdDep, booking_data: BookingsAddRequest):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f'Room with id: {booking_data.room_id} not found')
    if booking_data.date_from > booking_data.date_to:
        raise HTTPException(status_code=404, detail='date_from cannot be later than date_to')
    _booking_data = BookingsRequest(user_id=user_id, price=room.price, **booking_data.model_dump())
    res = await db.bookings.add(_booking_data)
    await db.commit()
    return res

