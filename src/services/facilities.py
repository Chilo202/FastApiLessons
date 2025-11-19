from src.exceptions import ObjectAlreadyExists, FacilityExistException
from src.services.base import BaseService


class FacilitiesService(BaseService):

    async def add_facilities(self, data):
        try:
            new_added_facilities = await self.db.facilities.add(data)
            await self.db.commit()

        except ObjectAlreadyExists:
            raise FacilityExistException
        return new_added_facilities


    async def get_all_facilities(self):
        return await self.db.facilities.get_all()