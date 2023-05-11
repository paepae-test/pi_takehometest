# import datetime
# from sqlalchemy import String
# from sqlalchemy.orm import Mapped, mapped_column

# from app.db.base import Base


# class AppUser(Base):
#     __tablename__ = "app_user"

#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
#     updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
#     is_active: Mapped[bool] = mapped_column(default=True)
#     username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
#     password: Mapped[str] = mapped_column(String(100))
