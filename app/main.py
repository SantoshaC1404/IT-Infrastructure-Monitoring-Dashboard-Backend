from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logger import logger, setup_logging

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)


@app.on_event("startup")
async def startup():
    logger.info("Application started")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Application stopped")
