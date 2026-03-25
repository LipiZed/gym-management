from app.models.base import Base, TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List

class Gym(Base, TimeStampMixin):
    __tablename__ = 'gyms'
    name: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255), unique = True)
    max_capacity: Mapped[int] = mapped_column()
    employees: Mapped[List['Employee']] = relationship(back_populates='gym')
    trainings: Mapped[List['Training']] = relationship(back_populates='gym')