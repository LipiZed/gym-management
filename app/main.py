from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.auth.router import router
from app.auth.service import create_first_admin
from app.core.database import AsyncSessionLocal
from app.gyms.router import router as gyms_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as db:
        await create_first_admin(db)
    yield

app = FastAPI(title="Gym Management System", lifespan=lifespan)

app.include_router(router)
app.include_router(gyms_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}