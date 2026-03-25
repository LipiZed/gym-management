from app.models.base import Base, TimeStampMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List



class TrainingType(Base, TimeStampMixin):
    __tablename__ = "training_types"
    name: Mapped[str] = mapped_column(String(255), unique = True)
    trainings: Mapped[List['Training']] = relationship(back_populates = 'training_type')