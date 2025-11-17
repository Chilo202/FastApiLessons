from src.api.dependencies import PaginationDep
from src.exceptions import check_date_to_after_date_from, HotelNotFound, ObjectNotFoundException, validate_date_from
from src.schemas.hotels import HotelAdd, HotelsPatch
from src.services.base import BaseService
from datetime import date


class HotelService(BaseService):

    async def get_filtered_by_time(self,
                                   location: str,
                                   title: str,
                                   date_from: date,
                                   date_to: date,
                                   pagination: PaginationDep):
        check_date_to_after_date_from(date_to, date_from)
        per_page = pagination.per_page or 5
        validate_date_from(date_from=date_from)
        return await self.db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
            offset=per_page * (pagination.page - 1),
            limit=per_page)

    async def update_hotel(self, hotel_model: HotelAdd, hotel_id: int):
        try:
            await self.db.hotels.edit(data=hotel_model, id=hotel_id)
            await self.db.commit()
        except ObjectNotFoundException:
            raise HotelNotFound

    async def update_hotel_particle(self, hotel_model: HotelsPatch, hotel_id: int, exclude_unset: bool):
        try:
            await self.db.hotels.edit(data=hotel_model, id=hotel_id, exclude_unset=exclude_unset)
            await self.db.commit()
        except ObjectNotFoundException:
            raise HotelNotFound

    async def delete_hotel(self, hotel_id):
        try:
            self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFound
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def get_hotel(self, hotel_id):
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFound

    async def get_hotel_check(self, hotel_id):
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFound
