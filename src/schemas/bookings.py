from pydantic import BaseModel, ConfigDict
from datetime import date


class BookingsAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingsRequest(BaseModel):
    user_id: int
    date_from: date
    date_to: date
    room_id: int
    price: int


class Bookings(BookingsRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)
