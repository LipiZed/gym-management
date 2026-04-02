from typing import List

from app.models.base import Base, TimeStampMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime



class Training(Base, TimeStampMixin):
    __tablename__ = 'trainings'
    type_id: Mapped[int] = mapped_column(ForeignKey('training_types.id'))
    gym_id: Mapped[int] = mapped_column(ForeignKey('gyms.id'))
    trainer_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))
    max_capacity: Mapped[int] = mapped_column()
    start_time: Mapped[datetime] = mapped_column()
    training_type: Mapped['TrainingType'] = relationship(back_populates = 'trainings')
    gym: Mapped['Gym'] = relationship(back_populates = 'trainings')
    trainer: Mapped['Employee'] = relationship(back_populates = 'trainings')
    bookings: Mapped[List['Booking']] = relationship(back_populates = 'training')