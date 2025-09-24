
from fastapi.params import Query
from fastapi import status, Response, APIRouter, Body

from repositories.hotels import HotelsRepository
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotels, HotelsPatch
from src.api.dependencies import PaginationDep
from sqlalchemy import insert, select, func

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
                              hotel_model: Hotels
                              ):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['name'] = hotel_model.name
            hotel['title'] = hotel_model.title
            return hotels
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"status": 'error', 'message': f"There is no Hotel with id: {hotel_id}"}


@router.patch("/{hotel_id}")
async def update_hotel_param(hotel_id: int,
                             response: Response,
                             hotel_data: HotelsPatch):
    global hotels
    if not hotel_data.title and not hotel_data.name:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": 'error', 'message': "No params for Patch"}
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            if hotel_data.title:
                hotel['title'] = hotel_data.title
            return hotels
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"status": 'error', 'message': f"There is no Hotel with id: {hotel_id}"}


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return hotels


@router.post("")
async def create_hotel(hotel_data: Hotels = Body(
    openapi_examples={
        "NewJersey": {"value":
                          {"title": "FreeJersey", "location": "12 ayre str."}},
        "Alyska": {"value":
                       {'title': "ColdJimmy", "location": "Bear street"}}
    })):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "Ok"}
