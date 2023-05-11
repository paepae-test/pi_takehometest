import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    name: Mapped[str] = mapped_column(String(50), index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
