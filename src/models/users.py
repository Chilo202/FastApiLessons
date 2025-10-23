import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from sqlalchemy import String, DateTime


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))
    nickname: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
