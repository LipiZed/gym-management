from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
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
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
    ):
    user = await service.authenticate_user(
        form_data.username, 
        form_data.password, 
        db
    )
    roles = []
    if user.client:
        roles.append("client")
    if user.employee:
        roles.append(user.employee.role)
    token_data = {"user_id": user.id, "email": user.email, "roles": roles}
    
    token = service.create_access_token(token_data)
    return {"access_token": token}
        