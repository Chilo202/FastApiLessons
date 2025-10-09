async def test_booking_me(authenticated_ac):
    response = await authenticated_ac.get("/bookings/me")
    print(response.status_code, response.json())


async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2025-10-10",
            "date_to": "2025-10-12"
        }
    )
    res = response.json()
    assert response.status_code == 200
    assert isinstance(res, dict)
    assert "data" in res
    assert res["data"]["room_id"] == room_id
