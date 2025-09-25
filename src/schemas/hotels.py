from pydantic import BaseModel, Field, ConfigDict


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotels(HotelAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class HotelsPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)

