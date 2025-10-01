from pydantic import BaseModel, ConfigDict, Field


class RoomsAddRequest(BaseModel):
    title: str = Field(min_length=3, )
    description: str | None = None
    price: int = Field(gt=0, description="Price should be bigger 0")
    quantity: int = Field(gt=0, description="Rooms should be greater 0")
    facilities_ids: list[int] | None = None


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str = Field(min_length=3)
    description: str | None = None
    price: int = Field(gt=0, description="Price should be bigger 0")
    quantity: int = Field(gt=0, description="Rooms should be greater 0")


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None,min_length=3)
    description: str | None = None
    price: int | None = Field(None, gt=0, description="Price should be bigger 0")
    quantity: int | None = Field(None, gt=0, description="Rooms should be greater 0")
    facilities_ids: list[int] | None = None



class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = Field(None,min_length=3)
    description: str | None = None
    price: int | None = Field(None, gt=0, description="Price should be bigger 0")
    quantity: int | None = Field(None, gt=0, description="Rooms should be greater 0")


class Rooms(RoomsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
