from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1.api import api_router
from app.core.config import settings

from app.core.exceptions.handlers import register_exception_handlers
from app.scheduler.monitoring_scheduler import start_monitoring_scheduler

# setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):

    # start_scheduler()

    start_monitoring_scheduler()

    yield

    # stop_scheduler()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

register_exception_handlers(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.REACT_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)


# @app.on_event("startup")
# async def startup():
#     logger.info("Application started")


# @app.on_event("shutdown")
# async def shutdown():
#     logger.info("Application stopped")
