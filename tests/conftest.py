import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()
import pytest
from httpx import AsyncClient, ASGITransport
from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, async_session_maker_null_pool
from src.database import engine_nullable_pool
from src.models import *
from src.main import app
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomsAdd
from src.schemas.facility import FacilityAddRequest
from src.utils.db_manager import DBManager


async def get_db_null_pull():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope='function')
async def db():
    async for db in get_db_null_pull():
        yield db


app.dependency_overrides[get_db] = get_db_null_pull


def get_mock_data(json_path: str):
    with open(json_path, "r") as data:
        return json.load(data)


@pytest.fixture(scope='session', autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(autouse=True, scope="session")
async def setup_database(check_test_mode):
    hotels = get_mock_data('tests/mock_hotels.json')
    rooms = get_mock_data('tests/mock_rooms.json')
    facilities = get_mock_data('tests/mock_facilities.json')
    async with engine_nullable_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomsAdd.model_validate(room) for room in rooms]
    facilities = [FacilityAddRequest.model_validate(facility) for facility in facilities]
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.facilities.add_bulk(facilities)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True, scope="session")
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": settings.USER_EMAIL,
            "password": settings.USER_PASSWORD,
            "first_name": "Gago",
            "last_name": "Beknazaryan",
            "nickname": "mr.robot"
        })


@pytest.fixture(autouse=True,scope="session")
async def authenticated_ac(ac, register_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/login",
                json=
                {"email":settings.USER_EMAIL,
                 "password": settings.USER_PASSWORD
                 }
                      )
        token = response.json().get("access_token")
        assert ac.cookies.get("access_token") == token
        yield ac


