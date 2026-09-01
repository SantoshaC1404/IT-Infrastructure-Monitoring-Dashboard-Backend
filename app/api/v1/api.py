from fastapi import APIRouter

from app.api.v1.routes import (
    auth_routes,
    device_routes,
    health_routes,
    dashboard_routes,
    users_routes,
    alert_routes,
    event_routes,
)

api_router = APIRouter()

api_router.include_router(health_routes.router)

api_router.include_router(auth_routes.router)

api_router.include_router(users_routes.router)

api_router.include_router(device_routes.router)

api_router.include_router(dashboard_routes.router)

api_router.include_router(alert_routes.router)

api_router.include_router(event_routes.router)
