


token = ''
async def test_registration(ac):
    response = await ac.post("auth/register", json={
        "email": "new@york.am",
        "password": "test1234",
        "first_name": "ARMAN",
        "last_name": "BARDUMYAN",
        "nickname": "BARD23",
    })
    assert response.status_code == 200
    assert response.json().get('status') == "OK"


async def test_login(ac):

    login_response = await ac.post("auth/login", json={
        "email": "new@york.am",
        "password": "test1234"
    })

    assert login_response.status_code == 200
    assert login_response.json().get('access_token')



async def test_user_logged(ac):
    logged_user_response = await ac.get("auth/me")
    assert logged_user_response.status_code == 200
    assert logged_user_response.json().get("email") == "new@york.am"


async def test_logout(ac):
    response = await ac.get("auth/logout")
    assert response.status_code == 200
    check_log_out = await ac.get("auth/me")
    assert check_log_out.json().get("detail") == "Unauthorized"


