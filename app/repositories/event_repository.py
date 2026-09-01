from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event


class EventRepository:

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create(self, event: Event):

        self.db.add(event)
        self.db.flush()

        return event

    # GET BY ID
    def get_by_id(self, event_id: int):

        stmt = select(Event).where(Event.id == event_id)

        return self.db.scalars(stmt).first()

    # LATEST EVENTS
    def latest(self, limit: int = 50):

        stmt = select(Event).order_by(Event.created_at.desc()).limit(limit)

        return list(self.db.scalars(stmt).all())

    # EVENTS FOR DEVICE
    def get_by_device(
        self,
        device_id: int,
        limit: int = 50,
    ):

        stmt = (
            select(Event)
            .where(Event.device_id == device_id)
            .order_by(Event.created_at.desc())
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())
