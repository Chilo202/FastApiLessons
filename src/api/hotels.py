from fastapi.params import Query
from fastapi import status, Response, APIRouter, Body
from repositories.hotels import HotelsRepository
from src.database import async_session_maker
from src.schemas.hotels import Hotels, HotelsPatch, HotelAdd
from src.api.dependencies import PaginationDep

router = APIRouter(prefix='/hotels', tags=['Hotels'])


# HOMEWORK #2
@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description='Hotel Title'),
        location: str | None = Query(None, description='Hotel Location')
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            offset=per_page * (pagination.page - 1),
            limit=per_page)


@router.put("/{hotel_id}")
async def update_hotel_params(hotel_id: int,
                              response: Response,
                              hotel_model: HotelAdd
                              ):
    async with async_session_maker() as session:
        res = await HotelsRepository(session).edit(data=hotel_model, id=hotel_id)
        await session.commit()
        if len(res) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"status": "error", "message": "Not found"}
        if len(res) > 1:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "error", "message": f"More than one found objects with that params "}
    return {"status": "ok"}


@router.patch("/{hotel_id}")
async def update_hotel_param(hotel_id: int,
                             hotel_data: HotelsPatch):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, response: Response):
    async with async_session_maker() as session:
        res = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    if len(res) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "error", "message": "Not found"}
    if len(res) > 1:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": f"More than one found objects with that params "}
    return {"status": "ok"}


@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(
    openapi_examples={
        "NewJersey": {"value":
                          {"title": "FreeJersey", "location": "12 ayre str."}},
        "Alyska": {"value":
                       {'title': "ColdJimmy", "location": "Bear street"}}
    })):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "inserted_data": hotel}

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await  HotelsRepository(session).get_one_or_none(id=hotel_id)
        return {"status": "OK", "hotel": hotel}
