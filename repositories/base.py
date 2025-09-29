from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError


class BaseRepository:
    model = None
    schema = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        res = await self.session.execute(query)
        return  [self.schema.model_validate(model) for model in res.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            res = await self.session.execute(add_data_stmt)
            model = res.scalars().one()
            return self.schema.model_validate(model)
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
