from repositories.base import BaseRepository
from src.models.booking import BookingsOrm
from src.schemas.bookings import Bookings


class BookingRepository(BaseRepository):
    model = BookingsOrm
    schema = Bookings


