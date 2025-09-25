import datetime

from fastapi import APIRouter

from repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.Users import UserRequestAdd, UserAdd
from passlib.context import CryptContext


router = APIRouter(prefix='/auth', tags=["Authorization and Autification"])
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password =pwd_context.hash(data.password)
    new_user_data = UserAdd(
        hashed_password=hashed_password,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        nickname=data.nickname,
    created_at=datetime.datetime.now())
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}