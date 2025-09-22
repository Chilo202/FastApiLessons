from pydantic import BaseModel, Field



class Hotels(BaseModel):
    title: str
    name: str


class HotelsPatch(BaseModel):
    title: str | None = Field(None)
    name: str | None = Field(None)

