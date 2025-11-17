from fastapi import APIRouter, Body
from fastapi.params import Query
from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import RoomNotFoundHttpException, HotelNotFoundHttpException, \
    HotelNotFound, RoomNotFound, ObjectAlreadyExists, ObjectAlreadyExistsHttp, HotelRoomNotFoundException, \
    HotelRoomNotFoundExceptionHttp, FacilitiesNotFoundException, FacilitiesNotFoundExceptionHttp
from src.schemas.rooms import RoomsAddRequest, RoomPatchRequest
from datetime import date

from src.services.rooms import RoomService

router = APIRouter(prefix="/hotel", tags=["Rooms"])


@router.get("/{hotel_id}/rooms", description="Get Rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2025-09-30"),
        date_to: date = Query(example="2025-10-07"),
):
    try:
        return await RoomService(db).get_rooms_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    except HotelNotFound:
        raise HotelNotFoundHttpException


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except HotelNotFound:
        raise HotelNotFoundHttpException
    except RoomNotFound:
        raise RoomNotFoundHttpException


@router.post("/{hotel_id}/rooms", description="Add new Rooms")
async def create_rooms(
        user_id: UserIdDep,
        hotel_id: int,
        db: DBDep,
        room_data: RoomsAddRequest = Body(
            example=(
                    {
                        "title": "Standart Room",
                        "description": "Its just Standart Room 16sqm",
                        "price": 5,
                        "quantity": 6,
                        "facilities_ids": [1, 2, 3],
                    }
            )
        ),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFound:
        raise HotelNotFoundHttpException
    except ObjectAlreadyExists:
        raise ObjectAlreadyExistsHttp
    except FacilitiesNotFoundException as e:
        raise FacilitiesNotFoundExceptionHttp(status_code=404, detail=e.detail)

    return {"status": "OK", "room": room}


@router.delete("/{hotel_id}/{room_id}", description="Delete Rooms")
async def delete_rooms(user_id: UserIdDep, hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomService(db).delete_room(room_id, hotel_id)
    except RoomNotFound:
        raise RoomNotFoundHttpException
    return {"status": "ok"}


@router.put("/{hotel_id}/{room_id}", description="Update Rooms")
async def update_rooms_params(
        user_id: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomsAddRequest = Body(
            example={
                "title": "Standart Room",
                "description": "Its just Standart Room 16sqm",
                "price": 5,
                "quantity": 6,
                "facilities_ids": [1, 2],
            }
        ),
):
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
    except RoomNotFound:
        raise RoomNotFoundHttpException
    except HotelNotFound:
        raise HotelNotFoundHttpException
    except HotelRoomNotFoundException:
        raise HotelRoomNotFoundExceptionHttp
    except FacilitiesNotFoundException as e:
        raise FacilitiesNotFoundExceptionHttp(status_code=404, detail=e.detail)

    return {"status": "ok"}


@router.patch("/{hotel_id}/{room_id}", description="Update Room param")
async def patch_room_param(
        userid: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    try:
        await RoomService(db).room_patch(hotel_id=hotel_id, room_id=room_id, room_data=room_data)

    except HotelNotFound:
        raise HotelNotFoundHttpException
    except HotelRoomNotFoundException:
        raise HotelRoomNotFoundExceptionHttp
    except RoomNotFound:
        raise RoomNotFoundHttpException
    except FacilitiesNotFoundException as e:
        raise FacilitiesNotFoundExceptionHttp(detail=e.detail)

    return {"status": "ok"}
