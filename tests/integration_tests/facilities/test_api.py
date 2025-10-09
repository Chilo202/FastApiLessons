



async def test_get_facilities(ac):
    response = await ac.get(url="/facilities")
    print(response.status_code, response.json())

async def test_add_facilities(ac):
    response = await ac.post(
        "/facilities",
        json={
            "title": "Kitchen"
        })
    print(response.json(), response.status_code)


