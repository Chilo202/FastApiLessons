from src.schemas.facility import FacilityAddRequest


async def test_add_facility(db):
    new_facility = FacilityAddRequest(title="Air Condition")
    new_added_facility = await db.facilities.add(new_facility)
    find_new_added_facility = await db.facilities.get_one_or_none(id=new_added_facility.id)
    assert find_new_added_facility

