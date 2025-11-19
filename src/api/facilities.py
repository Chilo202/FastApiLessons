from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.schemas.facility import FacilityAddRequest
from fastapi_cache.decorator import cache
from src.services.facilities import FacilitiesService
from src.exceptions import FacilityExistException, FacilityExistExceptionHttp
from src.api.dependencies import UserIdDep

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
async def get_all_facilities(db: DBDep):
    res = await FacilitiesService(db).get_all_facilities()
    return res


@cache(expire=10)
@router.post("")
async def add_facility(
        user_id: UserIdDep,
        db: DBDep,
        facilities_data: FacilityAddRequest = Body(
            openapi_examples={
                "Air_condition": {"value": {"title": "Air Condition"}},
                "Coffe_Machine": {"value": {"title": "Coffe Machine"}},
            }
        ),
):
    try:
        new_added_data = await FacilitiesService(db).add_facilities(data=facilities_data)
    except FacilityExistException as ex:
        raise FacilityExistExceptionHttp from ex
    return {"status": "OK", "data": new_added_data}
