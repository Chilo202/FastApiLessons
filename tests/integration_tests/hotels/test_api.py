





async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={"date_from": "2025-10-01", "date_to": "2025-10-05"})
    print(response.status_code, response.json())
