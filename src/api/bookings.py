from fastapi import APIRouter
from src.services.bookings import BookingService
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, \
    RoomNotFoundHttpException, AllRoomsAreBookedExceptionHttp
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAddRequest

router = APIRouter(prefix="/bookings", tags=["Book room"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_books()


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_books(user_id=user_id)


@router.post("")
async def book_room(db: DBDep, user_id: UserIdDep, booking_data: BookingsAddRequest):
    try:
        booking = await BookingService(db).book_room(booking_data=booking_data, user_id=user_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHttpException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedExceptionHttp
    return {"status": "OK", "data": booking}
