from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.gyms.schemas import GymCreate, GymResponse
from app.gyms.service import get_all_gyms, get_gym_by_id, create_gym
from app.auth.dependencies import require_role
router = APIRouter(prefix="/gyms", tags=["gyms"])

@router.get("/", response_model=list[GymResponse])
async def get_gyms(db: AsyncSession = Depends(get_db)):
    return await get_all_gyms(db)

@router.get("/{gym_id}", response_model=GymResponse)
async def get_gym(gym_id: int, db: AsyncSession = Depends(get_db)):
    gym = await get_gym_by_id(gym_id, db)
    if not gym:
        raise HTTPException(status_code=404, detail="Gym not found")
    return gym

@router.post("/")
async def create_gym_endpoint(gym: GymCreate, db: AsyncSession = Depends(get_db), user = Depends(require_role('admin'))):
    return await create_gym(gym, db)