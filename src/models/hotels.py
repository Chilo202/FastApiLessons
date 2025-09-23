from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from sqlalchemy import String, INTEGER


class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]



# class RoomsOrm(BaseOrm):
#     __tablename__ = 'rooms'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     room_number:[int] = mapped_column(INTEGER())
#     square: int = mapped_column()
#     level: int = mapped_column()
