from fastapi import APIRouter, Query, Body, HTTPException
from repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep, UserIdDep
from src.database import async_session_maker
from repositories.rooms import RoomRepository
from src.schemas.rooms import RoomsAdd, RoomsPatch

router = APIRouter(prefix='/rooms', tags=['Rooms'])


@router.get("", description='Get Rooms')
async def get_rooms(pagination: PaginationDep,
                    title: str | None = Query(None, description="Room Title"),
                    description: str | None = Query(None, description="Room Description"),
                    hotel_id: int | None = Query(None, description='Hotel id', ),
                    price: int | None = Query(None, description="Room price per Night", gt=1),
                    quantity: int | None = Query(None, description='Quantity free rooms', gt=1)
                    ):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        res = await RoomRepository(session).get_all(
            title=title,
            description=description,
            hotel_id=hotel_id,
            price=price,
            quantity=quantity,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )
        if len(res) == 0:
            return {"status": "OK", "message": "There is no Room with this criterias"}
        return res


@router.post("", description='Add new Rooms')
async def create_rooms(user_id: UserIdDep, data: RoomsAdd = Body(example=({
    "hotel_id": 4,
    "title": "Standart Room",
    "description": "Its just Standart Room 16sqm",
    "price": 5,
    "quantity": 6}
))):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=data.hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail=f'Hotel with id: {data.hotel_id} not found')
        res = await RoomRepository(session).add(data)
        await session.commit()

    return res


@router.delete("/{room_id}", description="Delete Rooms")
async def delete_rooms(user_id: UserIdDep, room_id: int):
    async with async_session_maker() as session:
        res = await RoomRepository(session).delete(id=room_id)
        await session.commit()
        if len(res) == 0:
            raise HTTPException(status_code=404, detail=f"Hotel with id: {room_id} not found")
        return {"status": "ok"}


@router.put('/{room_id}', description="Update Rooms")
async def update_rooms_params(user_id: UserIdDep, room_id: int, data: RoomsAdd = Body(example={
    "hotel_id": 4,
    "title": "Standart Room",
    "description": "Its just Standart Room 16sqm",
    "price": 5,
    "quantity": 6})):
    async with async_session_maker() as session:
        res = await RoomRepository(session).edit(data=data, exclude_unset=True, id=room_id)
        await session.commit()
        if not res:
            raise HTTPException(status_code=404, detail=f"Room with id{room_id} Not found")
    return {"status": "ok"}


@router.patch('/{room_id}', description="Update Room param")
async def patch_room_param(userid: UserIdDep, room_id: int, data: RoomsPatch):
    async with async_session_maker() as session:
        await RoomRepository(session).edit(data=data, id=room_id)
        await session.commit()

    return {"status": "ok"}
