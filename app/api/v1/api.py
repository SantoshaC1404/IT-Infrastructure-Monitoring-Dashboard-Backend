from fastapi import APIRouter

from app.api.v1.routes import auth_routes, device_routes, health_routes

api_router = APIRouter()

api_router.include_router(health_routes.router)

api_router.include_router(auth_routes.router)

api_router.include_router(device_routes.router)
