from fastapi import APIRouter, Body, HTTPException
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.rooms import RoomsAddRequest, RoomsAdd, RoomPatchRequest, RoomPatch

router = APIRouter(prefix='/hotel', tags=['Rooms'])


@router.get("/{hotel_id}/rooms", description='Get Rooms')
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


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
    "quantity": 6}
))):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail=f'Hotel with id: {hotel_id} not found')
    res = await db.rooms.add(_room_data)
    await db.commit()

    return res


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
                                  "quantity": 6})):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    res = await db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id)
    await db.commit()
    if not res:
        raise HTTPException(status_code=404, detail=f"Room with id{room_id} Not found")
    return {"status": "ok"}


@router.patch('/{hotel_id}/{room_id}', description="Update Room param")
async def patch_room_param(userid: UserIdDep, db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "ok"}
