async def test_get_facilities(ac):
    response = await ac.get(url="/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_add_facilities(ac):
    facility = "Kitchen"
    response = await ac.post(
        "/facilities",
        json={
            "title": facility
        })
    res = response.json()
    assert response.status_code == 200
    assert isinstance(res, dict)
    assert "data" in res
    assert res["data"]["title"] == facility

