from fastapi import FastAPI, Response, status

import uvicorn
from fastapi.params import Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "Sochi"},
    {"id": 2, "title": "Dubai", "name": "Dubai"},
    {"id": 3, "title": "NewJersey", "name": "NewJersey"},
    {"id": 4, "title": "Wilmington", "name": "Wilmington"}

]


@app.get('/')
async def func():
    return "HELLO WORLD"


@app.get('/{name}&{surname}')
async def hello(name, surname):
    return f"HELLO  {name, surname}"


@app.get('/hotels/')
async def get_hotels(
        id: int | None = Query(None, description='Hotel Id'),
        title: str | None = Query(None, description='Hotel Title')
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.put("/hotels/{hotel_id}")
async def update_hotel_params(hotel_id: int,
                              response: Response,
                              title: str = Body(description='Hotel Title'),
                              name: str = Body(description="Hotel Name"),
                              ):
    global hotels
    if not title or not name:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": 'error', 'message': "Title and Name is mandatory fields"}
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['name'] = name
            hotel['title'] = title
            return hotels
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"status": 'error', 'message': f"There is no Hotel with id: {hotel_id}"}


@app.patch("/hotels/{hotel_id}")
async def update_hotel_param(hotel_id: int,
                             response: Response,
                             title: str = Body(None, description='Hotel Title'),
                             name: str = Body(None, description="Hotel Name"),
                             ):
    global hotels
    if not title and not name:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": 'error', 'message': "No params for Patch"}
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if name:
                hotel["name"] = name
            if title:
                hotel['title'] = title
            return hotels
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"status": 'error', 'message': f"There is no Hotel with id: {hotel_id}"}

@app.delete('/hotels/{hotel_id}')
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return hotels


@app.post("/hotels")
async def create_hotel(title: str = Body(embed=True), ):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
