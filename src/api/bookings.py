from fastapi import APIRouter, HTTPException

from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, check_date_to_after_date_from
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAddRequest, BookingsRequest

router = APIRouter(prefix="/bookings", tags=["Book room"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def book_room(db: DBDep, user_id: UserIdDep, booking_data: BookingsAddRequest):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Room not found")
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    check_date_to_after_date_from(booking_data.date_to, booking_data.date_from)
    _booking_data = BookingsRequest(
        user_id=user_id, price=room.price, **booking_data.model_dump()
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException:
        raise HTTPException(status_code=409, detail="No available room for booking")
    await db.commit()
    return {"status": "OK", "data": booking}
