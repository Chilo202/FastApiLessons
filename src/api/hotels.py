from fastapi.params import Query
from fastapi import status, Response, APIRouter, Body, HTTPException
from src.schemas.hotels import HotelsPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from datetime import date
router = APIRouter(prefix='/hotels', tags=['Hotels'])


# HOMEWORK #2
@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Hotel Title"),
        location: str | None = Query(None, description="Hotel Location"),
        date_from: date = Query(example="2025-09-30"),
        date_to: date = Query(example="2025-10-07")

):

    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        title=title,
        location=location,
        date_from=date_from,
        date_to=date_to,
        offset= per_page * (pagination.page - 1),
        limit = per_page

    )


@router.put("/{hotel_id}")
async def update_hotel_params(hotel_id: int,
                              db: DBDep,
                              hotel_model: HotelAdd
                              ):
    res = await db.hotels.edit(data=hotel_model, id=hotel_id)
    await db.commit()
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def update_hotel_param(hotel_id: int,
                             db: DBDep,
                             hotel_data: HotelsPatch):
    await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, db: DBDep, response: Response):
    res = await db.hotels.delete(id=hotel_id)
    await db.commit()
    if len(res) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "error", "message": "Not found"}
    if len(res) > 1:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": f"More than one found objects with that params "}
    return {"status": "ok"}


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(
    openapi_examples={
        "NewJersey": {"value":
                          {"title": "FreeJersey", "location": "12 ayre str."}},
        "Alyska": {"value":
                       {'title': "ColdJimmy", "location": "Bear street"}}
    })):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "inserted_data": hotel}


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    hotel = await  db.hotels.get_one_or_none(id=hotel_id)
    return {"status": "OK", "hotel": hotel}
