from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.event.event_schema import EventResponse
from app.services.event.event_service import EventService

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get(
    "",
    response_model=list[EventResponse],
)
def get_events(
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
):

    service = EventService(db)

    return service.get_latest(limit)


@router.get(
    "/device/{device_id}",
    response_model=list[EventResponse],
)
def get_device_events(
    device_id: int,
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
):

    service = EventService(db)

    return service.get_device_events(
        device_id=device_id,
        limit=limit,
    )
