from datetime import date

from sqlalchemy.ext.hybrid import hybrid_property

from src.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey


class BookingsOrm(Base):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]

    @hybrid_property
    def total_cost(self):
        return self.price * (self.date_to - self.date_from).days
