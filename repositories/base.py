from sqlalchemy.ext.asyncio import async_sessionmaker

from sqlalchemy import select, insert


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

    async def add(self, **kwargs):
        data = insert(self.model).values(**kwargs).returning(self.model)
        res = await self.session.execute(data)
        return res.scalars().first()
