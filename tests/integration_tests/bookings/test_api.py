


async def test_booking_me(authenticated_ac):
    response = await authenticated_ac.get("/bookings/me")
    print(response.status_code, response.json())