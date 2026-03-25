from fastapi import FastAPI

app = FastAPI(title="Gym Management System")

@app.get("/health")
async def health_check():
    return {"status": "ok"}