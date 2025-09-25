from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name:str
    nickname:str
    created_at: datetime


class UserAdd(BaseModel):
    email:EmailStr
    first_name: str
    last_name:str
    nickname:str
    created_at: datetime
    hashed_password: str



class User(BaseModel):
    id:int


    model_config = ConfigDict(from_attributes=True)