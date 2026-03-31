from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.auth import service
from app.auth.schemas import TokenResponse, UserCreate, UserLogin, UserResponse
from app.core.database import get_db
from fastapi import HTTPException, status

from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await service.register_user(data, db)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await service.authenticate_user(data.email, data.password.get_secret_value(), db)
    roles = []
    if user.client:
        roles.append("client")
    if user.employee:
        roles.append(user.employee.role)
    token_data = {"user_id": str(user.id), "email": user.email, "roles": roles}
    
    return service.create_access_token(token_data)
    
        