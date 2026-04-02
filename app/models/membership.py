from app.models.base import Base, TimeStampMixin
from sqlalchemy import String, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
from enum import Enum


class MembershipStatus(str, Enum):
    ACTIVE = 'active'
    FROZEN = 'frozen'
    CANCELLED = 'cancelled'


class Membership(Base, TimeStampMixin):
    __tablename__ = 'memberships'
    type_id: Mapped[int] = mapped_column(ForeignKey("membership_plans.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    start_time: Mapped[datetime] = mapped_column()
    end_time: Mapped[datetime] = mapped_column()
    status: Mapped[MembershipStatus] = mapped_column(SAEnum(MembershipStatus))
    client: Mapped["Client"] = relationship(back_populates="memberships")
    membership_plan: Mapped["MembershipPlan"] = relationship(back_populates="memberships")