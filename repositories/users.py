
from pydantic import EmailStr

from repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.Users import User, UserWithHashedPassword

from sqlalchemy import select
class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User


    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        res = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if not model:
            return None
        return UserWithHashedPassword.model_validate(model)