from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, RoomNotFound, HotelNotFound, \
    ObjectAlreadyExists, validate_date_from, HotelRoomNotFoundException, FacilitiesNotFoundException
from src.schemas.facility import RoomFacilityAdd
from src.schemas.rooms import RoomsAdd, RoomPatch
from src.services.base import BaseService


class RoomService(BaseService):

    async def check_facilities(self, facilities_ids: list[int]):
        if len(facilities_ids) == 0:
            return
        for i in facilities_ids:
            try:
                await self.db.facilities.get_one(id=i)
            except ObjectNotFoundException:
                raise FacilitiesNotFoundException(i=i)

    async def get_rooms_filtered_by_time(self, hotel_id, date_from, date_to):

        check_date_to_after_date_from(date_to, date_from)
        validate_date_from(date_from)
        try:
            return await self.db.rooms.get_filtered_by_time(
                hotel_id=hotel_id, date_from=date_from, date_to=date_to
            )
        except ObjectNotFoundException:
            raise RoomNotFound

    async def get_room(self, hotel_id, room_id):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFound
        try:
            res = await self.db.rooms.get_room_with_facilities(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise RoomNotFound
        return res

    async def create_room(self, hotel_id, room_data):

        await self.check_facilities(room_data.facilities_ids)

        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFound
        try:
            _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))

            room = await self.db.rooms.add(_room_data)
            rooms_facilities = [
                RoomFacilityAdd(room_id=room.id, facility_id=f_id)
                for f_id in room_data.facilities_ids
            ]
            await self.db.rooms_facilities.add_bulk(rooms_facilities)
            await self.db.commit()
            return room
        except ObjectAlreadyExists:
            raise ObjectAlreadyExists

    async def delete_room(self, room_id, hotel_id):
        try:
            await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise RoomNotFound
        await self.db.commit()

    async def edit_room(self, hotel_id, room_id, room_data):
        await self.check_facilities(room_data.facilities_ids)

        _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
        try:
            await self.db.hotels.get_one(id=hotel_id)

        except ObjectNotFoundException:
            raise HotelNotFound
        try:
            room = await self.db.rooms.get_one(id=room_id)
            if room.hotel_id != hotel_id:
                raise HotelRoomNotFoundException
            await self.db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id)

        except ObjectNotFoundException:
            raise RoomNotFound

        await self.db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=room_data.facilities_ids
        )
        await self.db.commit()

    async def room_patch(self, hotel_id, room_id, room_data):
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(
            hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
        )
        await self.check_facilities(room_data.facilities_ids)
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFound
        try:
            room = await self.db.rooms.get_one(id=room_id)
            if room.hotel_id != hotel_id:
                raise HotelRoomNotFoundException

            await self.db.rooms.edit(
                data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
            )
        except ObjectNotFoundException:
            raise RoomNotFound
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()
