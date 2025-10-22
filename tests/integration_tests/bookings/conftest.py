import pytest

from tests.conftest import get_db_null_pull


@pytest.fixture(scope="session")
async def delete_all_bookings():
    async for _db in get_db_null_pull():
        await _db.bookings.delete()
        await _db.commit()
