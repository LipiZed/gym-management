from app.models.base import Base, TimeStampMixin
from sqlalchemy import ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from typing import List, Optional

class EmployeeRole(str, Enum):
    ADMIN = 'admin'
    TRAINER = 'trainer'
    
    
class Employee(Base, TimeStampMixin):
    __tablename__ = 'employees'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    gym_id: Mapped[Optional[int]] = mapped_column(ForeignKey('gyms.id'))
    role: Mapped[EmployeeRole] = mapped_column(SAEnum(EmployeeRole))
    user: Mapped["User"] = relationship(back_populates="employee")
    gym: Mapped["Gym"] = relationship(back_populates = 'employees')
    trainings: Mapped[List['Training']] = relationship(back_populates = 'trainer')