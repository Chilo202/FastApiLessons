from datetime import date

from fastapi import HTTPException


class AppErrors(Exception):

    detail = "Unexpected Error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(AppErrors):
    detail = "Object not found"


class AllRoomsAreBookedException(AppErrors):
    detail = "No available room for booking"


class DuplicateEntryError(AppErrors):
    detail = "Record with this unique value already exists."

class ObjectAlreadyExists(AppErrors):
    detail = "Object already exist"


class AppHttpsExceptions(HTTPException):
    detail = ""
    status_code = 500

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class HotelNotFound(AppHttpsExceptions):
    detail = "Hotel not Found"
    status_code = 404

class RoomNotFound(AppHttpsExceptions):
    detail = "Room not found"
    status_code = 404






def check_date_to_after_date_from(date_to: date, date_from: date):
    if date_to <= date_from:
        raise HTTPException(status_code=400, detail="date_to should be higher date_from")