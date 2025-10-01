from repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomFacilitiesOrm
from src.schemas.facility import Facility, RoomFacility
from sqlalchemy import select, insert, update, delete

class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility



class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesOrm
    schema = RoomFacility



    async def get_room_all_facilities_ids(self, room_id):
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(query)
        return res.scalars().all()


    async def delete_many_facilities_ids(self, room_id, facilities_id: list[int]):
        stmt = (
            delete(self.model)
            .where(self.model.room_id == room_id)
            .where(self.model.facility_id.in_(facilities_id))
        )
        res = await self.session.execute(stmt)

