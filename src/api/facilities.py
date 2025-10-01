from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAddRequest

router = APIRouter(prefix='/facilities', tags=['Facilities'])


@router.get('')
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post('')
async def add_facilities(
        db: DBDep,
        facilities_data: FacilitiesAddRequest = Body(
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
