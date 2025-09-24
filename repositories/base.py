from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        return res.scalars().get_one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        res = await self.session.execute(add_data_stmt)
        return res.scalars().one()

    async def edit(self, model_id: int, data: BaseModel):
        edit_data_stmt = update(self.model).where(self.model.id == model_id).values(**data.model_dump())
        return await self.session.execute(edit_data_stmt)

    async def delete(self, model_id: int):
        delete_data_stmt = delete(self.model).where(self.model.id == model_id)
        return await self.session.execute(delete_data_stmt)
