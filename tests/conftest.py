import pytest
from httpx import AsyncClient, ASGITransport
import json
from src.config import settings
from src.database import Base
from src.database import engine_nullable_pool
from src.models import *
from src.main import app
from sqlalchemy import insert


@pytest.fixture(autouse=True, scope="session")
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(autouse=True, scope="session")
async def setup_database():
    # hotels = get_mock_data('tests/mock_hotels.json')
    # rooms = get_mock_data('tests/mock_rooms.json')
    async with engine_nullable_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        # await conn.execute(insert(HotelsOrm), [hotel for hotel in hotels])
        # await conn.execute(insert(RoomsOrm), [room for room in rooms])

# def get_mock_data(json_path: str):
#     with open(json_path, "r") as data:
#         return json.loads(data.read())


@pytest.fixture(autouse=True, scope="session")
async def register_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "test33@gmail.com",
                "password": "test1234",
                "first_name": "Gago",
                "last_name": "Beknazaryan",
                "nickname": "mr.robot"
            })
