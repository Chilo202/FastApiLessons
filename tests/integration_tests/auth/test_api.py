import pytest


@pytest.mark.parametrize("email, password, first_name, last_name, nickname, status_code",
                         [("new@york.am", "test1234", "Gagik", "Martirosyan", "Bad23", 200),
                          ("new2@york.am", "test1234", "Karen", "Balansanyan", "Bad23", 200),
                          ("new2@york.am", "test1234", "Karen", "Balansanyan", "Bad23", 400),
                          ("new", "test1234", "Gagik", "Martirosyan", "Bad23", 422)
                          ])
async def test_auth_flow(ac, email, password, first_name, last_name, nickname, status_code):
    registration_response = await ac.post("auth/register", json={
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "nickname": nickname,
    })
    assert registration_response.status_code == status_code
    if registration_response.status_code != 200:
        return None
    assert "status" in registration_response.json()

    login_response = await ac.post("auth/login", json={
        "email": email,
        "password": password
    })

    assert login_response.status_code == status_code
    assert "access_token" in login_response.json()

    get_me_response = await ac.get("auth/me")
    assert get_me_response.status_code == status_code
    assert "email" in get_me_response.json()
    assert "first_name" in get_me_response.json()
    assert "last_name" in get_me_response.json()
    assert "nickname" in get_me_response.json()

    logout_response = await ac.get("auth/logout")
    assert logout_response.status_code == status_code
    assert "access_token" not in logout_response.cookies
