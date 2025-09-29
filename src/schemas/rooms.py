from pydantic import BaseModel, ConfigDict, Field


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str = Field(min_length=3,)
    description: str | None = None
    price: int = Field(gt=0, description="Price should be bigger 0")
    quantity: int = Field(gt=0, description="Rooms should be greater 0")


class Rooms(RoomsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)



class RoomsPatch(BaseModel):
    hotel_id: int
    title: str | None = Field(min_length=3,)
    description: str | None = None
    price: int | None = Field(gt=0, description="Price should be bigger 0")
    quantity: int | None = Field(gt=0, description="Rooms should be greater 0")

