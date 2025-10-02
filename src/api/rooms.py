from fastapi import APIRouter, Body, HTTPException
from fastapi.params import Query

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.facility import RoomFacilityAdd
from src.schemas.rooms import RoomsAddRequest, RoomsAdd, RoomPatchRequest, RoomPatch
from datetime import date

router = APIRouter(prefix='/hotel', tags=['Rooms'])


@router.get("/{hotel_id}/rooms", description='Get Rooms')
async def get_rooms(hotel_id: int,
                    db: DBDep,
                    date_from: date = Query(example='2025-09-30'),
                    date_to: date = Query(example='2025-10-07')
                    ):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    res = await db.rooms.get_filtered(id=room_id, hotel_id=hotel_id)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail=f"No data with hotel_id: {hotel_id} and room_id: {room_id}")
    return res


@router.post("/{hotel_id}/rooms", description='Add new Rooms')
async def create_rooms(user_id: UserIdDep, hotel_id: int, db: DBDep, room_data: RoomsAddRequest = Body(example=({
    "title": "Standart Room",
    "description": "Its just Standart Room 16sqm",
    "price": 5,
    "quantity": 6,
    "facilities_ids": [1, 2, 3]}
))):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail=f'Hotel with id: {hotel_id} not found')
    room = await db.rooms.add(_room_data)
    rooms_facilities = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities)
    await db.commit()

    return {"status": "OK", "room": room}


@router.delete("/hotel_id}/{room_id}", description="Delete Rooms")
async def delete_rooms(user_id: UserIdDep, hotel_id: int, room_id: int, db: DBDep):
    res = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    if len(res) == 0:
        raise HTTPException(status_code=404, detail=f"Hotel with id: {room_id} not found")
    return {"status": "ok"}


@router.put('/{hotel_id}/{room_id}', description="Update Rooms")
async def update_rooms_params(user_id: UserIdDep, db: DBDep, hotel_id: int, room_id: int,
                              room_data: RoomsAddRequest = Body(example={
                                  "title": "Standart Room",
                                  "description": "Its just Standart Room 16sqm",
                                  "price": 5,
                                  "quantity": 6,
                                  "facilities_ids": [1, 2]})):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()

    return {"status": "ok"}


@router.patch('/{hotel_id}/{room_id}', description="Update Room param")
async def patch_room_param(userid: UserIdDep, db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id=room_id, facilities_ids=_room_data_dict['facilities_ids'])
    await db.commit()

    return {"status": "ok"}
