from src.schemas.bookings import BookingsRequest
from datetime import date


async def test_add_booking(db):
    user_id = (await  db.user.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingsRequest(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=10, day=11),
        date_to=date(year=2025, month=10, day=20),
        price=100
    )
    new_added_booking = await db.bookings.add(booking_data)

    find_new_added_booking = await db.bookings.get_one_or_none(id=new_added_booking.id)
    assert find_new_added_booking
    updated_booking_data = BookingsRequest(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=10, day=11),
        date_to=date(year=2025, month=10, day=22),
        price=100
    )

    await db.bookings.edit(updated_booking_data, exclude_unset=True, id=find_new_added_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=find_new_added_booking.id)
    assert updated_booking
    assert updated_booking.id == new_added_booking.id
    assert updated_booking.date_to == updated_booking_data.date_to

    await db.bookings.delete(id=find_new_added_booking.id)
    booking = await db.bookings.get_one_or_none(id=find_new_added_booking.id)
    assert not booking

