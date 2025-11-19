from fastapi import APIRouter, Response
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.Users import UserRequestAdd, UserAdd, UserLogin
from src.services.auth import AuthService
from src.exceptions import (EmailNotRegisteredException, EmailORPasswordDoesNotMatchHttp,
                            PasswordDoesNotMatchException, EmailAlreadyRegisteredException,
                            EmailAlreadyRegisteredExceptionHttp)

router = APIRouter(prefix="/auth", tags=["Authorization and Autification"])


@router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    try:
        await AuthService(db).register(data)
    except EmailAlreadyRegisteredException as ex:
        raise EmailAlreadyRegisteredExceptionHttp from ex
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserLogin, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login(data)
    except EmailNotRegisteredException as ex:
        raise EmailORPasswordDoesNotMatchHttp from ex
    except PasswordDoesNotMatchException as ex:
        raise EmailORPasswordDoesNotMatchHttp from ex
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}



@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_me(user_id=user_id)


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "OK"}
