from src.models.booking import BookingsOrm
from src.models.facilities import FacilitiesOrm, RoomFacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Bookings
from src.schemas.facility import Facility, RoomFacility
from src.schemas.hotels import Hotels
from src.schemas.rooms import Rooms, RoomsWithRels
from src.schemas.Users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotels


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomsWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Bookings


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility

class RoomFacilityDataMapper(DataMapper):
    db_model = RoomFacilitiesOrm
    schema = RoomFacility