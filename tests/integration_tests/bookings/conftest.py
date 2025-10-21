import pytest
from src.database import engine_nullable_pool
from src.models.booking import BookingsOrm


@pytest.fixture(scope="session")
async def delete_all_bookings():
    async with engine_nullable_pool.begin() as conn:
        await conn.run_sync(BookingsOrm.__table__.drop, checkfirst=True)
        await conn.run_sync(BookingsOrm.__table__.create, checkfirst=True)
