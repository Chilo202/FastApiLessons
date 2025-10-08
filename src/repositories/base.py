from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by))
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in res.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if model is None:
            return None
        print(query.compile(compile_kwargs={"literal_binds": True} ))
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            res = await self.session.execute(add_data_stmt)
            model = res.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as e:
            '''Need some really good solution for here'''
            print(e)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data]).returning(self.model)
        try:
            await self.session.execute(add_data_stmt)
        except IntegrityError as e:
            '''Need some really good solution for here'''
            print(e)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_data_stmt = (update(self.model)
                            .filter_by(**filter_by)
                            .values(**data.model_dump(exclude_unset=exclude_unset))
                            .returning(self.model))
        res = await self.session.execute(update_data_stmt)
        return res.scalars().all()

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        res = await self.session.execute(delete_stmt)
        return res.scalars().all()
