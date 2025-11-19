from datetime import datetime, timedelta, timezone
from src.config import settings
from src.services.base import BaseService
from passlib.context import CryptContext
import jwt
from jwt.exceptions import ExpiredSignatureError
from src.exceptions import SignatureExpiredException, EmailNotRegisteredException, PasswordDoesNotMatchException, \
    EmailAlreadyRegisteredException, ObjectAlreadyExists, ObjectNotFoundException, UnAuthorizedUserException
from src.schemas.Users import UserLogin, UserRequestAdd, UserAdd


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_jwt(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except ExpiredSignatureError:
            raise SignatureExpiredException

    async def register(self, data: UserRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(
            hashed_password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            nickname=data.nickname,
            created_at=datetime.now(),
        )
        try:
            await self.db.user.add(new_user_data)
        except ObjectAlreadyExists:
            raise EmailAlreadyRegisteredException
        await self.db.commit()

    async def login(self, data: UserLogin):
        user = await self.db.user.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise PasswordDoesNotMatchException
        access_token = self.create_access_token(
            {"user_id": user.id, "user_name": user.first_name}
        )
        return access_token

    async def get_me(self, user_id):
        return await self.db.user.get_one(id=user_id)





