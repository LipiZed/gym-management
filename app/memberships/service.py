from datetime import timedelta

from fastapi import HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.dependencies import get_current_user
from app.memberships.schemas import MembershipPlanCreate, MembershipPlanResponse, MembershipCreate
from app.models import Membership
from app.models.membership import MembershipStatus
from app.models.membership_plan import MembershipPlan


async def get_all_membership_plans(db: AsyncSession):
    result = await db.execute(select(MembershipPlan))
    return result.scalars().all()

async def get_membership_plan_by_id(plan_id: int, db: AsyncSession):
    result = await db.execute(select(MembershipPlan).where(MembershipPlan.id == plan_id))
    plan = result.scalar_one_or_none()
    return plan


async def create_membership_plan(data: MembershipPlanCreate, db: AsyncSession):
    result = await db.execute(select(MembershipPlan).where(MembershipPlan.name == data.name))
    plan = result.scalar_one_or_none()
    
    if plan:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This gym already exists")
    
    new_plan = MembershipPlan(name = data.name, duration = data.duration, price = data.price)
    db.add(new_plan)
    await db.commit()
    await db.refresh(new_plan)
    
    response = MembershipPlanResponse.model_validate(new_plan)
    return response


async def create_membership(data: MembershipCreate, db: AsyncSession, user = Depends(get_current_user)):
    membership_plan = db.execute(select(MembershipPlan).where(MembershipPlan.id == data.type_id).scalar_one_or_none())
    membership_end_time = data.start_time + timedelta(days=membership_plan.duration)
    new_membership = Membership(type_id = data.type_id, client_id = user.client.id, start_time = data.start_time,
                                end_time = membership_end_time, status = MembershipStatus.ACTIVE)

    db.add(new_membership)
    await db.commit()
    await db.refresh(new_membership)
    response = MembershipPlanResponse.model_validate(new_membership)
    return response


async def get_my_memberships(db: AsyncSession, user = Depends(get_current_user)):
    result = await db.execute(select(Membership).where(Membership.client_id == user.client.id).options(selectinload(Membership.membership_plan)))
    memberships = result.scalars().all()
    return memberships