from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func
from src.schemas.hotels import Hotels


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotels



    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset) -> list[Hotels]:

        query = select(HotelsOrm)
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(func.lower(title)))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(func.lower(location)))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return[self.schema.model_validate(model) for model in result.scalars().all()]
