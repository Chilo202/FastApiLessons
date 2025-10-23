from datetime import datetime
from fastapi import APIRouter, HTTPException, Response
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.Users import UserRequestAdd, UserAdd, UserLogin
from src.services.auth import AuthService
from src.exceptions import DuplicateEntryError

router = APIRouter(prefix="/auth", tags=["Authorization and Autification"])


@router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(
        hashed_password=hashed_password,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        nickname=data.nickname,
        created_at=datetime.now(),
    )
    try:
        await db.user.add(new_user_data)
    except DuplicateEntryError:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    await db.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserLogin, response: Response, db: DBDep):
    try:
        user = await db.user.get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользватель с таким майлом не найден"
            )
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль не правильный")
        access_token = AuthService().create_access_token(
            {"user_id": user.id, "user_name": user.first_name}
        )
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    except:
        raise HTTPException(status_code=400)


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await db.user.get_one_or_none(id=user_id)


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "OK"}
