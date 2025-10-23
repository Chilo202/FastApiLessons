from pydantic import EmailStr
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.models.users import UsersOrm
from src.schemas.Users import UserWithHashedPassword
from sqlalchemy import select


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        res = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if not model:
            return None
        return UserWithHashedPassword.model_validate(model)
