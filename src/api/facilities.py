import json

from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.schemas.facility import FacilityAddRequest
from fastapi_cache.decorator import cache

router = APIRouter(prefix='/facilities', tags=['Facilities'])


@router.get('')
async def get_all_facilities(db: DBDep):
    res = await db.facilities.get_all()
    return res

@cache(expire=10)
@router.post('')
async def add_facility(
        db: DBDep,
        facilities_data: FacilityAddRequest = Body(
            openapi_examples={"Air_condition": {"value": {"title": "Air Condition"}
                                                },
                              "Coffe_Machine": {"value": {"title": "Coffe Machine"}
                                                }
                              }
        )
):
    new_added_data= await db.facilities.add(facilities_data)
    await db.commit()
    return {"status": "OK", "data": new_added_data}
