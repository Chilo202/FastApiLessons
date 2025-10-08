import json

from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facility import FacilityAddRequest
from src.tasks.tasks import test_task
from fastapi_cache.decorator import cache
router = APIRouter(prefix='/facilities', tags=['Facilities'])


@router.get('')
async def get_all_facilities(db: DBDep):
    facilities_cache = await redis_manager.get('facilities')
    print(f"{facilities_cache}")
    if not facilities_cache:
        facilities = await db.facilities.get_all()
        facilities_schema = [f.model_dump() for f in facilities_cache]
        facilities_json = json.dumps(facilities_schema)
        await redis_manager.set("facilities", facilities_json)
        return facilities
    facilities_dict = json.loads(facilities_cache)
    return facilities_dict


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
    await db.facilities.add(facilities_data)
    await db.commit()
    return {"status": "OK"}
