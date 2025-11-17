from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str = Field(min_length=1)
    location: str = Field(min_length=1)


class Hotels(HotelAdd):
    id: int


class HotelsPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
