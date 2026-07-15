from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logger import logger, setup_logging
from app.core.exception_handlers import register_exception_handlers

from app.scheduler.scheduler import (
    start_scheduler,
    stop_scheduler,
)

# setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):

    start_scheduler()

    yield

    stop_scheduler()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)


# @app.on_event("startup")
# async def startup():
#     logger.info("Application started")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Application stopped")
