from app.models.base import Base, TimeStampMixin
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from decimal import Decimal



class MembershipPlan(Base, TimeStampMixin):
    __tablename__ = 'membership_plans'
    name: Mapped[str] = mapped_column(String(255), unique = True)
    duration: Mapped[int] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    memberships: Mapped[List["Membership"]] = relationship(back_populates = 'membership_plan')