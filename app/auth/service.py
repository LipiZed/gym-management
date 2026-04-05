from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import selectinload
from app.auth.schemas import UserCreate
from app.core.config import settings
import bcrypt
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import Employee, EmployeeRole
from app.models.user import User
from app.models.client import Client
from fastapi import HTTPException, status


def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def create_access_token(data: dict):
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {**data, "exp": expire_time}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


async def register_user(data: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    new_hashed_password = hash_password(data.password.get_secret_value())
    new_user = User(email=data.email, hashed_password=new_hashed_password, full_name=data.full_name,
                    phone = data.phone, is_active=True)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    new_client = Client(user_id = new_user.id)
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "is_active": new_user.is_active,
        "full_name": new_user.full_name,
        "phone": new_user.phone,
    }



async def authenticate_user(email: str, password: str, db: AsyncSession):
    result = await db.execute(
        select(User)
        .where(User.email == email)
        .options(selectinload(User.client), selectinload(User.employee))
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return user


async def create_first_admin(db: AsyncSession):
    result = await db.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
    user = result.scalar_one_or_none()
    if user:
        print("Admin already exists, skipping...")
        return

    new_hashed_password = hash_password(settings.ADMIN_PASSWORD)
    new_user = User(email=settings.ADMIN_EMAIL, hashed_password=new_hashed_password, is_active=True)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    new_employee = Employee(user_id = new_user.id, role = EmployeeRole.ADMIN)
    db.add(new_employee)
    await db.commit()
    await db.refresh(new_employee)