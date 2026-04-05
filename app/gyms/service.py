from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.gyms.schemas import GymCreate
from app.models.gym import Gym


async def get_all_gyms(db: AsyncSession):
    stmt = select(Gym)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_gym_by_id(gym_id: int, db: AsyncSession):
    result = await db.execute(select(Gym).where(Gym.id == gym_id))
    gym = result.scalar_one_or_none()
    return gym


async def create_gym(data: GymCreate, db: AsyncSession):
    result = await db.execute(select(Gym).where(Gym.name == data.name))
    gym = result.scalar_one_or_none()
    
    if gym:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This gym already exists")
    
    new_gym = Gym(name = data.name, location = data.location, max_capacity = data.max_capacity)
    db.add(new_gym)
    await db.commit()
    await db.refresh(new_gym)
    
    return {
        "gym_id": new_gym.id,
        "gym_name": new_gym.name,
        "gym_location": new_gym.location,
        "gym_max_capacity": new_gym.max_capacity
    }