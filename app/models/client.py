from app.models.base import Base, TimeStampMixin
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class Client(Base, TimeStampMixin):
    __tablename__ = 'clients'
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    full_name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(30), unique = True)
    user: Mapped["User"] = relationship(back_populates="client")
    memberships: Mapped[List['Membership']] = relationship(back_populates='client')
    bookings: Mapped[List['Booking']] = relationship(back_populates = 'client')