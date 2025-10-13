from fastapi import FastAPI

from api.auth import router as auth_router
from api.users import router as users_router
from api.gyms import router as gym_router
from api.trainers import router as trainer_router
from api.trainer_gyms import router as trainer_gyms_router

from models import create_tables

app = FastAPI(title='FitFindr', description='API for getting all data')

app.include_router(auth_router, prefix='/api/v1')
app.include_router(users_router, prefix='/api/v1')
app.include_router(gym_router, prefix='/api/v1')
app.include_router(trainer_router, prefix='/api/v1')
app.include_router(trainer_gyms_router, prefix='/api/v1')


@app.on_event("startup")
async def startup_event():
    create_tables()
    print("✅ Database tables created!")

@app.get('/')
async def get():
    return {"message": "FitFindr API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FitFindr API"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)