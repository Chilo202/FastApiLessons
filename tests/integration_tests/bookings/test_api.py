import pytest

@pytest.mark.parametrize("room_id, date_from, date_to, status_code ", [
    (1, "2025-10-10", "2025-10-17", 200),
    (1, "2025-10-10", "2025-10-17", 200),
    (1, "2025-10-10", "2025-10-17", 200),
    (1, "2025-10-10", "2025-10-17", 200),
    (1, "2025-10-10", "2025-10-17", 200),
    (1, "2025-10-10", "2025-10-17", 500)])
async def test_add_booking(db, authenticated_ac, room_id, date_from, date_to, status_code):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert "data" in res
        assert res["data"]["room_id"] == room_id

@pytest.mark.parametrize("room_id, date_from, date_to, bookings_count ", [
    (1, "2025-10-10", "2025-10-17", 1,),
    (1, "2025-10-10", "2025-10-17", 2),])
async def test_booking_me(authenticated_ac,
                          delete_all_bookings,
                          room_id,
                          date_from,
                          date_to,
                          bookings_count):
    book_room = await authenticated_ac.post("/bookings",
                                            json={
                                                "room_id": room_id,
                                                "date_from": date_from,
                                                "date_to": date_to
                                            })
    assert book_room.status_code == 200
    response_my_bookings = await authenticated_ac.get("/bookings/me")
    assert bookings_count == len(response_my_bookings.json())
