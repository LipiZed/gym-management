from app.models.base import Base, TimeStampMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

class User(TimeStampMixin, Base):
    __tablename__ = 'users'
    email: Mapped[str] = mapped_column(String(255), unique = True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default = True)
    client: Mapped[Optional["Client"]] = relationship(back_populates = 'user', uselist=False)
    employee: Mapped[Optional["Employee"]] = relationship(back_populates = 'user', uselist=False)