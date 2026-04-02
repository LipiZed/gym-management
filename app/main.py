from fastapi import FastAPI
from app.auth.router import router


app = FastAPI(title="Gym Management System")

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}