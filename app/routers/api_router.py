from fastapi import APIRouter

from app.routers import user, device_data

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user.router)
api_router.include_router(device_data.router)