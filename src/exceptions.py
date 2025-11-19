from datetime import date

from fastapi import HTTPException


class AppErrors(Exception):
    detail = "Unexpected Error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(AppErrors):
    detail = "Object not found"


class SignatureExpiredException(AppErrors):
    detail = "Token signature expired"


class UnAuthorizedUserException(AppErrors):
    detail = "Authentication required"
    status_code = 401


class AllRoomsAreBookedException(AppErrors):
    detail = "No available room for booking"


class EmailAlreadyRegisteredException(AppErrors):
    detail = "Email already registered"


class EmailNotRegisteredException(AppErrors):
    detail = "Email does not exist"


class PasswordDoesNotMatchException(AppErrors):
    detail = "Password does not match"


class DuplicateEntryError(AppErrors):
    detail = "Record with this unique value already exists."


class ObjectAlreadyExists(AppErrors):
    detail = "Object already exist"


class HotelNotFound(AppErrors):
    detail = "Hotel not found"



class RoomNotFound(AppErrors):
    detail = "Room not found"


class HotelRoomNotFoundException(AppErrors):
    detail = "Room with the specified ID does not exist in this hotel."


class FacilityExistException(AppErrors):
    detail = "Facility already exists."


class FacilitiesNotFoundException(AppErrors):

    def __init__(self, i):
        self.detail = f"Facility with id:{i} not found:"


class AppHttpsExceptions(HTTPException):
    detail = ""
    status_code = 500

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class FacilitiesNotFoundExceptionHttp(HTTPException):
    status_code = 404
    detail = "Facility not found"


class HotelNotFoundHttpException(AppHttpsExceptions):
    detail = "Hotel not Found"
    status_code = 404


class RoomNotFoundHttpException(AppHttpsExceptions):
    detail = "Room not found"
    status_code = 404


class ObjectAlreadyExistsHttp(AppHttpsExceptions):
    detail = "Object already exist"
    status_code = 400


class AllRoomsAreBookedExceptionHttp(AppHttpsExceptions):
    detail = "No available room for booking "
    status_code = 404


class SignatureExpiredExceptionHttp(AppHttpsExceptions):
    detail = "Token signature expired"
    status_code = 401


class HotelRoomNotFoundExceptionHttp(AppHttpsExceptions):
    detail = "Room with the specified ID does not exist in this hotel."
    status_code = 409


class EmailORPasswordDoesNotMatchHttp(AppHttpsExceptions):
    detail = "Email or password does not exist"
    status_code = 404


class EmailAlreadyRegisteredExceptionHttp(AppHttpsExceptions):
    detail = "Email already registered"
    status_code = 404


class UnAuthorizedUserExceptionHttp(AppHttpsExceptions):
    detail = "Authentication required"
    status_code = 401

class FacilityExistExceptionHttp(AppHttpsExceptions):
    detail = "Facility already exists."
    status_code = 404


def check_date_to_after_date_from(date_to: date, date_from: date):
    if date_to <= date_from:
        raise HTTPException(status_code=400, detail="date_to should be higher date_from")


def validate_date_from(date_from: date):
    if date_from < date.today():
        raise HTTPException(status_code=404, detail="date_from cannot be earlier than today")
