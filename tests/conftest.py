import pytest
from httpx import AsyncClient, ASGITransport
import json
from src.config import settings
from src.database import Base, async_session_maker_null_pool
from src.database import engine_nullable_pool
from src.models import *
from src.main import app
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomsAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope='function')
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


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
    async with engine_nullable_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomsAdd.model_validate(room) for room in rooms]
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True, scope="session")
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "test33@gmail.com",
            "password": "test1234",
            "first_name": "Gago",
            "last_name": "Beknazaryan",
            "nickname": "mr.robot"
        })
