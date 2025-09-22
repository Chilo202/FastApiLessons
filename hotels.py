from fastapi.params import Query
from fastapi import status, Response, APIRouter
from schemas.hotels import Hotels, HotelsPatch

router = APIRouter(prefix='/hotels', tags=['Hotels'])

hotels = [
    {"id": 1, "title": "Sochi", "name": "Sochi"},
    {"id": 2, "title": "Dubai", "name": "Dubai"},
    {"id": 3, "title": "NewJersey", "name": "NewJersey"},
    {"id": 4, "title": "Wilmington", "name": "Wilmington"},
    {"id": 5, "title": "Munich", "name": "Munich"},
    {"id": 6, "title": "Yerevan", "name": "Yerevan"},
    {"id": 7, "title": "Rome", "name": "Rome"},
    {"id": 8, "title": "Florance", "name": "Florance"}
]


# HOMEWORK #2
@router.get('', response_model=list[Hotels])
async def get_hotels(
        id: int | None = Query(None, description='Hotel Id'),
        title: str | None = Query(None, description='Hotel Title'),
        page: int | None = Query(None, description='Start Page'),
        per_page: int | None = Query(10, description='PerPage')
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    if not page:
        return hotels[:per_page]
    # PAGINATION LOGIC
    if page:
        start = (page - 1) * per_page
        end = page * per_page
        return hotels[start:end]
    else:
        return hotels[:per_page]


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
async def create_hotel(hotel_data: Hotels):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
