from app.models.base import Base, TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum as SAEnum
from typing import List
from enum import Enum


class BookingStatus(str, Enum):
    ACTIVE = 'active'
    CANCELLED = 'cancelled'



class Booking(Base, TimeStampMixin):
    __tablename__ = 'bookings'
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    training_id: Mapped[int] = mapped_column(ForeignKey('trainings.id'))
    status: Mapped[BookingStatus] = mapped_column(SAEnum(BookingStatus))
    training: Mapped['Training'] = relationship(back_populates = 'bookings')
    client: Mapped['Client'] = relationship(back_populates='bookings')