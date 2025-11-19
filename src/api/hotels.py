from fastapi.params import Query
from fastapi import Response, APIRouter, Body
from src.services.hotels import HotelService
from src.exceptions import HotelNotFoundHttpException, HotelNotFound
from src.schemas.hotels import HotelsPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from datetime import date

router = APIRouter(prefix="/hotels", tags=["Hotels"])


# HOMEWORK #2
@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Hotel Title"),
        location: str | None = Query(None, description="Hotel Location"),
        date_from: date = Query(example="2025-09-30"),
        date_to: date = Query(example="2025-10-07"),
):
    return await HotelService(db).get_filtered_by_time(
        location,
        title,
        date_from,
        date_to,
        pagination)


@router.put("/{hotel_id}")
async def update_hotel_params(hotel_id: int, db: DBDep, hotel_model: HotelAdd):
    try:
        await HotelService(db).update_hotel(hotel_model, hotel_id)
    except HotelNotFound:
        raise HotelNotFoundHttpException
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def update_hotel_param(hotel_id: int, db: DBDep, hotel_data: HotelsPatch):
    try:
        await HotelService(db).update_hotel_particle(hotel_model=hotel_data, hotel_id=hotel_id, exclude_unset=True)
        await db.commit()
    except HotelNotFound:
        raise HotelNotFoundHttpException

    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep, response: Response):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except HotelNotFound:
        raise HotelNotFoundHttpException
    return {"status": "ok"}


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(
            openapi_examples={
                "NewJersey": {"value": {"title": "FreeJersey", "location": "12 ayre str."}},
                "Alyska": {"value": {"title": "ColdJimmy", "location": "Bear street"}},
            }
        ),
):
    hotel = await HotelService(db).create_hotel(hotel_data)

    return {"status": "OK", "inserted_data": hotel}


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except HotelNotFound:
        raise HotelNotFoundHttpException
