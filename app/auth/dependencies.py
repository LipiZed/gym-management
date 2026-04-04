from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        payload_user_id = payload.get('user_id')
        result = await db.execute(
            select(User)
            .where(User.id == payload_user_id)
            .options(selectinload(User.client), selectinload(User.employee)))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    

def require_role(*roles: str):
    async def checker(user = Depends(get_current_user)):
        user_roles = []
        if user.client:
            user_roles.append("client")
        if user.employee:
            user_roles.append(user.employee.role.value)
        if not any(role in roles for role in user_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return user
    return checker

